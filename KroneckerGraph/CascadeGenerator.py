# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 16:40
# @Author  : zxl
# @FileName: CascadeGenerator.py

import numpy as np

class CascadeGenerator():

    def __init__(self):
        pass

    def GenerateCascade(self,G,source_num,cascade_per_source,node_per_source):
        """
        给定有向图G，生成source_num*cascade_per_source个cascade
        :param G: 有向图:{node:{neighor1:prob,neighbor2:prob,...}}
        :param source_num: 源节点数目
        :param cascade_per_source: 每个源节点生成的source数目
        :param node_per_source: 每个cascade中结点数目
        :return: {s1:[path1,path2,...],s2:[...]}
        """
        source_lst=[]
        for item in set(G.keys()):
            source_lst.append(item)
            if len(source_lst)==source_num:
                break
        res={}
        for s  in source_lst:
            res[s]=self.ProbWalk(G,s,cascade_per_source,node_per_source)
        return res

    def DFS(self,G,source,step):
        """
        在图G上，以source为起点，再走step步
        :param G: 待游走的图{node:{neighor1:prob,neighbor2:prob,...}}
        :param source: 源节点
        :param step: 再走step步
        :return:
        """
        res=[]

        if step==0 or source not in G.keys() or len(G[source].keys())==0 or (len(G[source].keys())==1 and source in G[source].keys()):#不用走或者没法走的时候，停止
            return []
        neighbor_lst=list(G[source].keys())
        weight_lst=[]
        for neighbor in neighbor_lst:
            weight_lst.append(G[source][neighbor])
        norm_weigh_lst=[w/np.sum(weight_lst) for w in weight_lst]
        next_source=source
        while next_source==source:#自己不能传播给自己
            next_source=np.random.choice(neighbor_lst,1,p=norm_weigh_lst)[0]

        res.append(next_source)
        for item in self.DFS(G,next_source,step-1):
            res.append(item)
        return res


    def ProbWalk(self,G,source,cascade_num,node_num):
        """
        给定source，生成cascade_num个cascade，每个cascade中node_num个结点
        :param G: 待游走的图
        :param source: 源节点
        :param cascade_num: 待生成的cascade数目
        :param node_num: 每个cascade中结点数目
        :return: [path1,path2,...]
        """
        res=[]
        neighbor_lst=list(G[source].keys())
        weight_lst=[]
        for neighbor in neighbor_lst:
            weight_lst.append(G[source][neighbor])
        norm_weight_lst=[x/np.sum(weight_lst) for x in weight_lst]

        source_lst=np.random.choice(neighbor_lst,cascade_num,p=norm_weight_lst)
        for source in source_lst:
            cur_path=[source]
            for v in self.DFS(G,source,node_num-1):
                cur_path.append(v)
            res.append(cur_path)
        return res
