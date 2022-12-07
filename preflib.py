# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 12:02:34 2022

@author: SariolaDisaA
"""
#requires pip3 install preflibtools
import networkx as nx

from preflibtools.instances import OrdinalInstance
import numpy as np

# We can populate the instance by reading a file from PrefLib.
# You can do it based on a URL or on a path to a file

#This dataset contains the results of surveying students at AGU University of Science and Technology about their course preferences.
# Each student provided a rank ordering over all the courses with no missing elements. 
#There are 9 courses to choose from in 2003 and 7 in 2004.
instance1 = OrdinalInstance()
instance2 = OrdinalInstance()

instance1.parse_file("agh/00009-00000001.soc")
instance2.parse_file("agh/00009-00000002.soc")
subset_color = [
    "gold",
    "violet",
    "limegreen",
    "darkorange",
]
def maximal_matching_multipartite(G):
    r"""Find a maximal threepart matching in the graph.

    A matching is a subset of edges in which no node occurs more than once.
    A maximal matching cannot add more edges and still be a matching.

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph

    Returns
    -------
    matching : set
        A maximal matching of the graph.
    """
    matching = set()
    nodes = set()
    all_nodes = np.array(G.nodes())
    all_edges = G.edges()
    nodes_1 = set(all_nodes[0:8]) #these are very naive and static, but since this is just for proof of implementation
    #It does not need further exploration
    nodes_3 = set(all_nodes[9:16])

    pairs_weights = {}
    max_sums = []
    max_sums_pairs = []
    index = 0
    #1st we work through all possible pairs and generate an nxmxv matrix to show all the possible combinations for the sums
    pairs, weights = {}, {}
    taken = set()
    for one in nodes_1:      
        temp_sum = []
        temp_pairs = []
        for two in G[one].keys():
            weight_1 = G[one][two]['weight']
            if one not in weights:
                weights[one] = weight_1
                pairs[one] = two
                taken.add(two)
                
            elif weights[one] < weight_1:
                if one in taken:
                    key_list = list(pairs.keys())
                    val_list = list(pairs.values())
                    val = val_list.index(one)
                    key = key_list[val]
                    
                    if weights[key] < weight_1:
                    
                        weights[one] = weight_1
                        pairs[one] = two
                        taken.add(two)
                           
            for three in nodes_3:
                weight_2 = G[two][three]['weight']
                if two not in weights:
                    weights[two] = weight_2
                    pairs[two] = three
                    taken.add(three)
                    
                elif weights[two] < weight_2:
                    if two in taken:
                        key_list = list(pairs.keys())
                        val_list = list(pairs.values())
                        print(val_list, taken, two)
                        val = val_list.index(two)
                        key = key_list[val]
                        print(key, two)
                        if weights[key] < weight_2:
                        
                            weights[two] = weight_2
                            pairs[two] = three
                            taken.add(two)
                            taken.remove(key)
    print(pairs)
                
                #temp_sum.append(weight_1 + weight_2)
                #temp_pairs.append((one,two,three)) #
        #max_sums.append(np.array(temp_sum)) #this is the vector for all the choices for node ones  sums
        #max_sums_pairs.append(np.array(temp_pairs))#this is the vector for all the choices for node ones pairs, same index correspondance as for max_sums
    #max_sums = np.array(max_sums) #could initialise in the beginning as numpy to clean the code up, but not worth it right now
    #max_sums_pairs = np.array(max_sums_pairs)
    #print(max_sums, max_sums_pairs)
    #print(max_sums.shape, max_sums_pairs.shape)
    #work through the matrix again to find max combination
    #max_sum = 0
    #pairs = set()
    #all_sums = []
    #all_pairs = {}
    #for index, val in enumerate(max_sums):
        #max_val =np.argpartition(val, 10)[-10:]
        #ten_max = max_val[np.argsort(val[max_val])][::-1] #sort it in the correct order
        #all_sums.append(ten_max)
        #print(ten_max)
        #print(max_sums_pairs[index][ten_max])
        #print(max_sums[index][ten_max])
        #all_pairs
            
        
        
                    
                    
                
    for edge in G.edges():
        # If the edge isn't covered, add it to the matching
        # then remove neighborhood of u and v from consideration.
        u, v = edge
        #print(G.get_edge_data(u, v))

        if u not in nodes and v not in nodes and u != v:
            matching.add(edge)
            nodes.update(edge)
    return matching
#We assume that for every student, we have a weight to preference based on the order of their rank,
#So weight 1 = rank 1, weight 0 = rank 9
B = nx.Graph()

for i in instance1.alternatives_name:
    B.add_node(f'Course {i}-1', subset=1)
    
for i in instance2.alternatives_name:
    B.add_node(f'Course {i}-2', subset=3)
for index, val in enumerate(instance1.multiplicity):
    
    B.add_node(index, subset=2)
    for index2, course in enumerate(val):
        B.add_edge(index, f'Course {course[0]}-1', weight = (1/len(val))* (len(val)-index2), color ='black') #normalise weight of preference between two years to be comparable
    if index > 10:
        break
for index, val in enumerate(instance2.multiplicity):

    for index2, course in enumerate(val):
        B.add_edge(index, f'Course {course[0]}-2', weight = (1/len(val))* (len(val)-index2), color ='black') #normalise weight of preference between two years to be comparable
    
    if index > 10:
        break
    
matching = maximal_matching_multipartite(B) 
#matching = nx.max_weight_matching(B)
for edge in matching:
    B.add_edge(edge[1],edge[0], color = 'red', weight= 10)
colors = nx.get_edge_attributes(B,'color').values()

pos = nx.multipartite_layout(B, subset_key='subset')
color = [subset_color[data["subset"]] for v, data in B.nodes(data=True)]

nx.draw(B, pos, node_color=color,edge_color= colors, with_labels=True)