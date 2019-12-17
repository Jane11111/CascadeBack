# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 15:08
# @Author  : zxl
# @FileName: test.py

import random
import numpy as np
import networkx as nx

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

def ShortestPath(s, L):
    """
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
                res[t] =np.array([])
            res[t]=np.append(res[t],path_length[t])
    return res


G={1:{2:0.2,3:0.3,4:0.4},2:{3:0.5,4:0.6},3:{4:0.2}}

L=Sample(3,5,G)
print(L)

shortest_path=ShortestPath(1,L)
print(shortest_path)