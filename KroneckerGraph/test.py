# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 15:08
# @Author  : zxl
# @FileName: test.py

import random
import numpy as np


def InverseSample( alpha, k, num):
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


alpha=0.8
k=5
num=10
res=InverseSample(alpha,k,num)
print(res)

