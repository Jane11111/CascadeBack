# -*- coding: utf-8 -*-
# @Time    : 2019/12/17 15:49
# @Author  : zxl
# @FileName: SourceDetection.py

import numpy as np

class SourceDetection():

    def __init__(self):
        pass

    def InferTime(self,s,c,L,G):
        """
        给定source s，以及部分观测到的一条cascade c，采样的集合L，图G，推断，如果以s为源，最可能的ts，以及对应似然值
        :param s: node
        :param c: {node1:t1,node2:t2,...}
        :param L: 每条边k个值[{node:{neighbor1:[],neighbor2:[],...}}
        :param G: {node:{neighbor1:alpha,neighbor2:alpha,...}}
        :return: （ts,likelihood_v）or (None,None)表示该节点不可能作为source
        """
        return(None,None)

    def InverseSample(self,alpha,k,num):
        """
        根据参数为alpha，超参数为k的概率密度函数，采样num个样本
        :param alpha: f的参数
        :param k: f的超参数
        :param num: 样本数目
        :return:
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


