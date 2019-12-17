# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 15:08
# @Author  : zxl
# @FileName: test.py

import random
import numpy as np


def InverseSample(alpha, k, num):
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


def Sample( k, l, G):
    """
    返回L
    :param s: node
    :param l: 采样的数目
    :param G: {node:{neighbor1:alpha,neighbor2:alpha,...}}
    :return:每条边采样L个值，返回集合: {node:{neighbor1:[],neighbor2:[],...}}
    """
    L = G
    for node in G.keys():
        for neighbor in G[node].keys():
            alpha = G[node][neighbor]
            sample_arr = InverseSample(alpha, k, l)
            L[node][neighbor] = sample_arr
    return L

G={1:{2:0.2,3:0.3,4:0.4},2:{3:0.5,4:0.6},3:{4:0.2}}

L=Sample(3,10,G)
print(L)