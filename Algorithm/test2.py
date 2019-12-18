# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 16:01
# @Author  : zxl
# @FileName: test2.py


import numpy as np

lst=[1,2,3]
print(lst)
lst.insert(0,-np.inf)
lst.append(float(np.inf))
print(lst)
print(lst[-1]==np.inf)