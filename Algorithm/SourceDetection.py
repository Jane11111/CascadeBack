# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 15:49
# @Author  : zxl
# @FileName: SourceDetection.py

import networkx as nx
import numpy as np

class SourceDetection():

    def __init__(self,G):
        """
        初始化一些图，便于后续计算
        :param G: {node:{neighbor1:alpha,neighbor2:alpha,...}}
        """
        inverse_G={}
        for u in G.keys():
            for v in G[u].keys():
                if v not in inverse_G.keys():
                    inverse_G[v]=[]
                inverse_G[v].append(u)
        self.inverse_G=inverse_G
        self.G=G
        V_set=set([])
        for u in G.keys():
            V_set.add(u)
            for v in G[u].keys():
                V_set.add(v)
        self.V=list(V_set)

    def InferSourceTime(self,D,k,l):
        """
        给定由同一个源节点产生的cascade集合C，找出最可能的源节点，以及该源结点下每个cascade最可能的产生时间ts
        :param D: 由同一个源节点产生的cascade集合[cascade1,cascade2,...],cascade={node1:t1,node2:t2,...}
        :param k: 函数f的超参数
        :param l: 采样数目
        :return:s,[tc1_s,tc2_s,...]源节点，以及每个cascade对应的时间
        """
        G=self.G
        #采样
        L=self.Sample(k,l,G)
        #首先找M：有O做父亲的隐藏结点,
        M=set([])#TODO D中所有node称之为O，M为非O的隐藏结点，并且有O作为父亲
        O=set([])#TODO 只能解释为D中所有的
        for cascade in D:
            for u in cascade:
                O.add(u)
                sons =list(G[u].keys())#O的儿子
                for v in sons:
                    M.add(v)
        M=M.difference(O)

        res_s=None
        max_likelihood=-1
        res_ts_lst=[]
        for s in M:#所有结点都试一下

            (ts_lst,likelihood)=self.InferTime(s,D,L,G)#以s为源，推断所有的cascade时间，及其似然

            if likelihood>max_likelihood:#找到了更优的source
                res_s=s
                max_likelihood=likelihood
                res_ts_lst=ts_lst
        return (res_s,res_ts_lst)


    def InferTime(self,s,D,L,G):
        """
        给定source s，以及部分观测到的一条cascade c，采样的集合L，图G，推断，如果以s为源，最可能的ts，以及对应似然值
        :param s: node
        :param D: 具有同一个源节点的cascade集合，[{node1:t1,node2:t2,...},{},{},...]
        :param L: 每条边k个值{node:{neighbor1:[],neighbor2:[],...}}
        :param G: {node:{neighbor1:alpha,neighbor2:alpha,...}}
        :return: （ts_lst,likelihood）其中ts_lst表示D中所有cascade对应的最可能的ts list，likelihood表示以s为源的最大似然；or (None,None)表示该节点不可能作为source
        """

        u=list(L.keys())[0]
        v=list(L[u].keys())[0]
        l=len(L[u][v])

        path_length=self.ShortestPath(s,L)#{node1:[],node2:[],...}相当于采样的t #TODO 以s为源，对每个node找l个最可能infected的时间


        #找到所有的change point，基于c和 path_length
        All_O=set([])#D中所有观测到的结点
        for cascade in D:
            for node in cascade.keys():
                All_O.add(node)

        change_point_lst=[]
        for i in All_O:
            #TODO 这个按照每个cascade中出现的结点计算change point，确实能够包含所有qingk
            #TODO 但是同时也会增加很多区间，因为每个cascade单独计算的ts
            for cascade in D:#TODO 因为ti在不同的cascade中值不同，所以每个都计算下
                if i not in cascade :
                    continue
                ti=cascade[i]
                for j in self.getParent(i):#所有的父亲
                    for sample_l in range(l):#i的父亲采样的，所有可能infected的时间
                        tjl=path_length[j][sample_l]#父亲j这个结点对应第sample_l个样本值
                        if ti-tjl<=0:
                            continue
                        change_point_lst.append(ti-tjl)
        change_point_lst.sort()#从小到大排序


        ts_lst=[]
        likelihood=1
        #对于每两个change point对应的区间，可以对应一个\phi L （ts）式子，然后后面就是对这个式子求解了。
        change_point_lst.append(np.inf)#最后一个区间是 无穷大
        change_point_lst.insert(0,0)#第一个区间是 负无穷到某个值
        for cascade in D:#TODO 对每个cascade都应该有一个ts
            opt_ts=None
            max_likelihood=-1
            O = set([])  # TODO 当前cascade中观测到的结点
            M = set([])  # TODO 相对于上面的O而言的H，并且有O作为父亲
            for u in cascade.keys():
                O.add(u)
                for v in self.getParent(u):
                    M.add(v)
            M = M.difference(O)
            O_left_lst=[]
            O_right_lst=[]#不变
            M_up_left_lst=[]#不随ts改变，随采样大小而改变，与M_down_left_lst等价
            M_up_right_lst=[]
            M_down_left_lst=[]#不随ts改变，随采样大小而改变，与M_up_left_lst等价
            M_down_right_lst=[]#不随ts改变，随采样大小而改变
            # TODO fixted_formula =XXX 处理O_right_lst这个列表

            l_lst_dic={}
            for cur_l in range(l):
                for i in M:
                    parent_set=self.getParent(i)
                    for j in parent_set.difference(O):
                        if path_length[j][cur_l]<path_length[i][cur_l]:
                            M_up_left_lst.append(j)
                            M_down_left_lst.append(j)

                    for j in parent_set.intersection(O):
                        if path_length[j][cur_l]<path_length[i][cur_l]:
                            M_down_right_lst.append(j)
                l_lst_dic[cur_l]={}
                l_lst_dic[cur_l]['m_up_left_lst']=M_up_left_lst
                l_lst_dic[cur_l]['m_down_left_lst']=M_down_left_lst
                l_lst_dic[cur_l]['m_down_right_lst']=M_down_right_lst
            # TODO ts_fixted_formula=XXX #处理不随分段值而改变的列表

            for idx in np.arange(1,len(change_point_lst)):#分段求解
                formula = None
                # 找到区间
                a = change_point_lst[idx - 1]
                b = change_point_lst[idx]
                for cur_l in range(l):
                    for i in O:#TODO 这个O感觉应该是对当前这个cascade的O
                        parent_set=set(self.getParent(i))
                        left_lst=[]#pi_i \ O
                        for j in parent_set.difference(O):
                            if path_length[j][cur_l]+a+0.5*(b-a)>=cascade[i]:
                                continue
                            left_lst.append(j)
                        #TODO formula=XXXXXX #处理O_left_lst这个列表
                    for i in M:#TODO 对应上面O
                        parent_set=set(self.getParent(i))
                        M_up_right_lst=[]
                        for j in parent_set.intersection(O):
                            if cascade[j]>=path_length[i][cur_l]+a+0.5*(b-a):
                                continue
                            M_up_right_lst.append(j)
                        #TODO formula=XXXX #处理M_up_right_lst这个列表
                    #TODO formula=XXXX    #综合多个列表


                cur_ts,cur_likelihood=self.Solve(formula,a,b)#就是给当前段最优解
                if cur_likelihood>max_likelihood:#当前这个段的解比前面的都好
                    max_likelihood=cur_likelihood
                    opt_ts=cur_ts
            ts_lst.append(opt_ts)
            likelihood*=max_likelihood

        return (ts_lst,likelihood)

    def Solve(self,formula,a,b):
        """
        给出equ（8）的表达式，求解使其最大的ts值，以及对应似然值
        :param formula: equ（8）对应不同区间的形式
        :param a: ts最小值，包含
        :param b: ts最大值，不包含
        :return: (ts,likelihood)，最优ts，以及对应likelihood
        """
        #TODO 如何求解，怎么化为一个指数函数
        ts=0
        likelihood=0
        return (ts,likelihood)

    def getParent(self,v):
        """
        给定图G，找到图中结点v的父亲结点
        :param v: node
        :param G: 有向图，{node:{neighbor1:alpha,neighbor2:alpha,...}}
        :return: set,[node1,node2,node3]
        """
        return set(self.inverse_G[v])


    def InverseSample(self,alpha,k,num):
        """
        根据参数为alpha，超参数为k的概率密度函数，采样num个样本
        :param alpha: f的参数
        :param k: f的超参数
        :param num: 样本数目
        :return:服从于f的num个样本 ndarray
        """
        uniform_arr = np.random.uniform(0, 1, num)
        res = alpha * (-np.log(1 - uniform_arr)) ** (1.0 / k)
        return res


    def Sample(self,k,l,G):
        """
        返回L
        :param k: 超参数
        :param l: 采样的数目
        :param G: {node:{neighbor1:alpha,neighbor2:alpha,...}}
        :return:每条边采样L个值，返回集合: {node:{neighbor1:[],neighbor2:[],...}}
        """
        L=G
        for node in G.keys():
            for neighbor in G[node].keys():
                alpha=G[node][neighbor]
                sample_arr=self.InverseSample(alpha,k,l)
                L[node][neighbor]=sample_arr
        return L

    def ShortestPath(self,s,L):
        """
        #TODO 这么写对每一个source都会重新生成一个network 图，没有必要，后续可以在某个函数里面生成，然后作为参数传过来。
        基于L个采样的样本，
        给定源节点s，找出该结点到其他点的最短路径，权重由L中采样结果给出
        :param s: 源节点
        :param L:{node:{neighbor1:[],neighbor2:[],...}}
        :return: {node1:[],node2:[]}
        """
        u = list(L.keys())[0]
        v = list(L[u].keys())[0]
        weight_num = len(L[u][v])  # 样本的数目
        # 构造networkx中网络形式
        res = {}
        for i in range(weight_num):
            edge_lst = []
            for u in L.keys():
                for v in L[u].keys():
                    edge_lst.append([u, v, L[u][v][i]])

            G = nx.DiGraph()
            G.add_weighted_edges_from(edge_lst)
            path_length = nx.single_source_dijkstra_path_length(G, s, weight='weight')
            for t in path_length.keys():
                if t not in res.keys():
                    res[t] = np.array([])
                res[t] = np.append(res[t], path_length[t])
        return res
