# -*- coding: utf-8 -*-
# @Time    : 2019/12/14 17:53
# @Author  : zxl
# @FileName: main.py

import random
import numpy as np
from KroneckerGraph.KroneckerGraphGenerator import KroneckerGraphGenerator
from KroneckerGraph.CascadeGenerator import CascadeGenerator
from Algorithm.ParameterInference import ParameterInference
from Algorithm.SourceDetection import SourceDetection

if __name__ =="__main__":
    # initiator=np.array([[0.5,0.5],[0.5,0.5]])
    # initiator=np.array([[0.9,0.5],[0.5,0.3]])
    initiator = np.array([[0.9, 0.1], [0.9, 0.1]])
    node_num = 256
    edge_num = 1000
    generator = KroneckerGraphGenerator()
    graph = generator.GenerateGraph(initiator, node_num, edge_num)
    print("--------initial graph--------------")
    print(graph)


    prob_graph = {}
    for k in graph.keys():
        neighbor_lst = list(graph[k])
        weight_lst = [1.0 / len(neighbor_lst) for i in range(len(neighbor_lst))]
        prob_graph[k] = {neighbor_lst[i]: weight_lst[i] for i in range(len(neighbor_lst))}

    cascade_generator = CascadeGenerator()
    source_num=1
    cascade_per_source=5
    node_per_cascade=10
    cascade_dic = cascade_generator.GenerateCascade(prob_graph, source_num, cascade_per_source, node_per_cascade)
    print("------------initial path--------")
    print(cascade_dic)

    #将这些完整的cascade转为t那个向量

    C={}
    for s in cascade_dic.keys():
        C[s]=[]
        for path in cascade_dic[s]:
            cur_dic = {}
            for  i in range(len(path)):
                if path[i] not in cur_dic.keys():
                    cur_dic[path[i]]=i+1#只记录初次infected的时间
            C[s].append(cur_dic)

    print("---------------- cascade lst C   ----------------")
    print(C)

    print("---------- cascade with the same source D -----------------------")
    source=list(C.keys())[0]
    D=[]
    for cascade in C[source]:
        incomplete_cascade={}
        for u in cascade.keys():
            if u==source:
                continue
            incomplete_cascade[u]=cascade[u]
        D.append(incomplete_cascade)
    print("source:%d"%source)
    print("cascade lst: "+str(D))

    # 测试Algorithm 1
    print("---------parameter inference alpha-------------")
    par_infer=ParameterInference()
    G=par_infer.infer(prob_graph,C)#带alpha的图
    print(G)
    print("---------------source detection----------------")
    sd=SourceDetection(G)
    l=3
    k=2
    s,ts_lst=sd.InferSourceTime(D,k,l)
    print("source: "+str(s))
    print("ts lst: "+str(ts_lst))

