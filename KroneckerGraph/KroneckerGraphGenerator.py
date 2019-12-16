# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 14:44
# @Author  : zxl
# @FileName: KroneckerGraphGenerator.py

import numpy as np
import pandas as pd

class KroneckerGraphGenerator:

    def __init__(self):
        """
        初始化
        :param initiator:初始化参数矩阵,ndarray
        :param node_num: 合成网络结点数目
        :param edge_num: 合成网络边数目
        """


    def GenerateGraph(self,initiator,node_num,edge_num):
        """
        生成满足要求的图
        :return: 邻接链表
        """
        # TODO 按道理来讲这里的base应该是初始矩阵的大小
        iter_num = int(np.log2(node_num))
        arr=self.GraphKrockerProduct(initiator,iter_num)
        arr=self.Sample(arr,edge_num)
        res={}
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if arr[i,j]==0:
                    continue
                if i not in res.keys():
                    res[i]=[]
                res[i].append(j)
        return res

    def GraphKrockerProduct(self,initiator,iter_num):
        """
        生成合成网络的邻接矩阵
        :return:网络的邻接矩阵表示，ndarray (node_num * node_num)
        """
        last_arr=initiator
        n=len(initiator)
        for iter in range(iter_num-1):
            d = len(initiator) * len(last_arr)

            cur_arr = np.full(shape=(d, d), fill_value=0.0)
            for i in range(len(cur_arr)):
                for j in range(len(cur_arr[0])):
                    i1 = i // n
                    j1 = j // n
                    i2 = i % n
                    j2 = j % n
                    cur_arr[i, j] = last_arr[i1, j1] * initiator[i2, j2]
            last_arr = cur_arr
        return last_arr



    def Sample(self,arr,edge_num):
        """
        给定概率邻接矩阵，从中采样slef.edge_num个样本
        :param arr: 概率邻接矩阵，值表示该边存在概率
        :param edge_num: 目标图中边条数
        :return: arr：ndarray，1表示有边，0表示无边
        """
        weight_lst=arr.flatten()
        norm_weight_lst=[x/np.sum(weight_lst) for x in weight_lst]
        sample_idx_lst=np.random.choice(len(weight_lst),edge_num,replace=False,p=norm_weight_lst)

        n = len(arr)
        res=np.full(shape=arr.shape,fill_value=0)

        for v in sample_idx_lst:
            i=v//n
            j=v%n
            res[i,j]=1
        return res




