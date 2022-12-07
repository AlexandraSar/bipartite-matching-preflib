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
        A non-optimal maximal matching of the graph.
    """
    matching = set()
    nodes = set()
    all_nodes = np.array(G.nodes())
    all_edges = G.edges()
    nodes_1 = set(all_nodes[0:9]) #these are very naive and static, but since this is just for proof of implementation
    
    #It does not need further exploration
    nodes_3 = set(all_nodes[9:16])

    #1st we work through all possible pairs and generate an nxmxv matrix to show all the possible combinations for the sums
    pairs, weights = {}, {}
    taken_1 = set()
    taken_2 = set()
    changes = False
    index=1

    #We divide the graph vertices into three independent sets, courses 1 in set 1, people in set 2 and courses 2 in set 3
    #We iterate through all of these sets comparing whether the iterated match is better than the vertices existing pair. 
    #as we are looking to maximise the sums of the two chosen ones, we are working through them in two phases
    #This could be improved on by prioritising matches for people who have a match on the otherside of the graph when it comes to course selection
    #So in a way, this is NOT the optimal maximal set, but implementing it would not be too difficult
    
    #The code has also a lot of repetition, and could easily be cut down and modularised, since we redo work
    while True:
        index +=1
        changes = False
        for one in nodes_1:
        
            for two in G[one].keys():
                
                weight_1 = G[one][two]['weight']
                if one not in weights.keys(): #i.e. if we do not have a pairfor set 1 vertex v, we assume we do not have to deal with a pairs old pairs
                    changes = True
                    weights[one] = 0
                    if two not in taken_1:
                        weights[one] = weight_1
                        if one in pairs.keys():
                            taken_1.remove(pairs[one])
                        pairs[one] = two
                        taken_1.add(two)
                        
                if weights[one] < weight_1:
                    if two not in taken_1:
                        changes = True
                        weights[one] = weight_1
                        if one in pairs.keys():
                            taken_1.remove(pairs[one])
                        pairs[one] = two
                        taken_1.add(two)
                    


                            
                    if two in taken_1:
                        
                        key_list = list(pairs.keys())
                        val_list = list(pairs.values())
                        val = val_list.index(two)

                        key = key_list[val]
                        
                        if weights[key] < weight_1:
                            changes = True
                            
                            if one in pairs.keys():
                                taken_1.remove(pairs[one])
                            weights[one] = weight_1
                            pairs[one] = two

                            taken_1.add(two)

                            del pairs[key]
                            weights[key] = 0
                        
                            
                               
                for three in nodes_3:
                    weight_2 = G[two][three]['weight']
                    if two not in weights.keys():
                        changes = True
                        weights[two] = 0
                        if three not in taken_2:
                            weights[two] = weight_2
                            pairs[two] = three
                            taken_2.update([three, two])
                            
                        
                    if weights[two] < weight_2:
                        if three not in taken_2:
                            changes = True
                            weights[two] = weight_2
                            pairs[two] = three
                            taken_2.add(three)
                        
                        if three in taken_2:
                            
                            key_list = list(pairs.keys())
                            val_list = list(pairs.values())
                            try: #This is just lazy debugging, as im missing a remove somewhere, or it is not being triggered
                                val = val_list.index(three)
                            except ValueError:
                                taken_2.remove(three)
                            #print(pairs)
                            #print(taken)
                            key = key_list[val]
                            
                            #print(key, two)
                            if weights[key] < weight_2:
                                changes = True
                                weights[two] = weight_2
                                pairs[two] = three
                                
                                taken_2.update([three, two])

                                taken_2.remove(pairs[key])
                                del pairs[key]
                                weights[key] = 0
        print(len(taken_2), index)
        if changes == False and len(taken_1) == 9 and len(taken_2) == 13:
            break
    return list(pairs.items())
    print(pairs)
                
                    
                
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
