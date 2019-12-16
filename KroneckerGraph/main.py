# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 17:53
# @Author  : zxl
# @FileName: main.py

import random
import numpy as np
from KroneckerGraph.KroneckerGraphGenerator import KroneckerGraphGenerator
from KroneckerGraph.CascadeGenerator import CascadeGenerator

if __name__ =="__main__":
    # initiator=np.array([[0.5,0.5],[0.5,0.5]])
    # initiator=np.array([[0.9,0.5],[0.5,0.3]])
    initiator = np.array([[0.9, 0.1], [0.9, 0.1]])
    node_num = 256
    edge_num = 1000
    generator = KroneckerGraphGenerator()
    graph = generator.GenerateGraph(initiator, node_num, edge_num)

    prob_graph = {}
    for k in graph.keys():
        neighbor_lst = list(graph[k])
        weight_lst = [1.0 / len(neighbor_lst) for i in range(len(neighbor_lst))]
        prob_graph[k] = {neighbor_lst[i]: weight_lst[i] for i in range(len(neighbor_lst))}

    cascade_generator = CascadeGenerator()
    cascade_dic = cascade_generator.GenerateCascade(prob_graph, 2, 2, 40)
    for s in cascade_dic.keys():
        print(prob_graph[s])
        for path in cascade_dic[s]:
            print(path)

    #将这些完整的cascade转为t那个向量

    new_cascade_dic={}
    for s in cascade_dic.keys():
        new_cascade_dic[s]={}
        for path in cascade_dic[s]:
            for  i in range(len(path)):
                if path[i] not in new_cascade_dic[s].keys():
                    new_cascade_dic[s][path[i]]=i#只记录初次infected的时间
            print(path)
            print(new_cascade_dic[s])

