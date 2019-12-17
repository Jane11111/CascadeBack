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
        :param L: [{node:{neighbor1:t,neighbor2:t,...}},{}]
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


    def Sample(self,s,k,G):
        """
        返回L
        :param s: node
        :param k: f函数超参数
        :param G: {node:{neighbor1:alpha,neighbor2:alpha,...}}
        :return:每条边采样一个值，返回集合: [{node:{neighbor1:t,neighbor2:t,...}},{}]
        """
        L=[]
        return L


