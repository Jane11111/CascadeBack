# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 15:08
# @Author  : zxl
# @FileName: test.py

import random
import numpy as np

from KroneckerGraph.KroneckerGraphGenerator import KroneckerGraphGenerator
from KroneckerGraph.CascadeGenerator import CascadeGenerator

# initiator=np.array([[0.5,0.5],[0.5,0.5]])
# initiator=np.array([[0.9,0.5],[0.5,0.3]])
initiator=np.array([[0.9,0.1],[0.9,0.1]])
node_num=256
edge_num=512
generator=KroneckerGraphGenerator()
graph=generator.GenerateGraph(initiator,node_num,edge_num)

prob_graph={}
for k in graph.keys():
    neighbor_lst=list(graph[k])
    weight_lst=[1.0/len(neighbor_lst) for i in range(len(neighbor_lst))]
    prob_graph[k]={neighbor_lst[i]:weight_lst[i] for i in range(len(neighbor_lst))}


cascade_generator=CascadeGenerator()
cascade_dic=cascade_generator.GenerateCascade(prob_graph,2,2,40)
for s in cascade_dic.keys():
    print(prob_graph[s])
    for path in cascade_dic[s]:
        print(path)



