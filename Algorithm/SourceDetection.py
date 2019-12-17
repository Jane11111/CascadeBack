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

    def InferSourceTime(self,C,k,l):
        """
        给定由同一个源节点产生的cascade集合C，找出最可能的源节点，以及该源结点下每个cascade最可能的产生时间ts
        :param C: 由同一个源节点产生的cascade集合[cascade1,cascade2,...],cascade={node1:t1,node2:t2,...}
        :param k: 函数f的超参数
        :param l: 采样数目
        :return:s,[tc1_s,tc2_s,...]源节点，以及每个cascade对应的时间
        """
        G=self.G
        #采样
        L=self.Sample(k,l,G)
        #首先找M：有O做父亲的隐藏结点
        M=set([])
        O=set([])
        for cascade in C:
            for u in cascade:
                O.add(u)
                sons =list(G[u].keys())#O的儿子
                for v in sons:
                    M.add(v)
        M=M.difference(O)

        res_s=None
        max_likelihood=-1
        res_ts_lst=[]
        for s in M:
            cur_likelihood=1
            cur_ts_lst=[]
            for cascade in C:
                (ts,likelihood)=self.InferTime(s,cascade,L,G)
                cur_ts_lst.append(ts)
                cur_likelihood*=likelihood
            if cur_likelihood>max_likelihood:#找到了更优的source
                res_s=s
                max_likelihood=cur_likelihood
                res_ts_lst=cur_ts_lst
        return (res_s,res_ts_lst)


    def InferTime(self,s,c,L,G):
        """
        给定source s，以及部分观测到的一条cascade c，采样的集合L，图G，推断，如果以s为源，最可能的ts，以及对应似然值
        :param s: node
        :param c: {node1:t1,node2:t2,...}
        :param L: 每条边k个值{node:{neighbor1:[],neighbor2:[],...}}
        :param G: {node:{neighbor1:alpha,neighbor2:alpha,...}}
        :return: （ts,likelihood_v）or (None,None)表示该节点不可能作为source
        """
        path_length=self.ShortestPath(s,L)#{node1:[],node2:[],...}相当于采样的t

        #找到所有的change point，基于c和 path_length

        change_point_lst=[]

        change_point_lst.sort()



        #对于每两个change point对应的区间，可以对应一个\phi L （ts）式子，然后后面就是对这个式子求解了。

        ts=0
        likelihood=0
        return (ts,likelihood)


    def getNeighbor(self,v):
        """
        给定图G，找到图中结点v的父亲结点
        :param v: node
        :param G: 有向图，{node:{neighbor1:alpha,neighbor2:alpha,...}}
        :return: list,[node1,node2,node3]
        """
        return self.inverse_G[v]


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
