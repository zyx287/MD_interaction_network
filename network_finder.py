import re
import os
import networkx as nx
os.chdir(r"/home/hipeson/data2/zhangyuxiang/test/GCT")
# Interaction.csv contains the interaction network
with open("interaction.CSV", "r") as f:
    data = f.readlines()
# Data Structure
interactions = []
source_of_lists = []
target_of_lists = []
for elem in data:
    elem = elem.split(',')
    frame = int(elem[0])
    interaction_type = elem[1]
    source = elem[2]
    target = elem[3]
    
    source_elem = source.split(':')
    source_chain_id = source_elem[0]
    source_res_name = source_elem[1]
    source_res_num = int(source_elem[2])
    source_atom_name = source_elem[3]
    source_data = {
        'chain_id': source_chain_id,
        'res_name': source_res_name,
        'res_num': source_res_num,
        'atom_name': source_atom_name
    }

    target_elem = target.split(':')
    target_chain_id = target_elem[0]
    target_res_name = target_elem[1]
    target_res_num = int(target_elem[2])
    target_atom_name = target_elem[3]
    target_data = {
        'chain_id': target_chain_id,
        'res_name': target_res_name,
        'res_num': target_res_num,
        'atom_name': target_atom_name
    }

    interactions.append({
        'frame': frame,
        'interaction_type': interaction_type,
        'source': source_data,
        'target': target_data
    })
# Building the Graph: G for DiGraph, H for Graph
G = nx.DiGraph()
for interaction in interactions:
    source_node = "{}:{}:{}".format(
        interaction['source']['chain_id'],
        interaction['source']['res_name'],
        interaction['source']['res_num']
    )
    target_node = "{}:{}:{}".format(
        interaction['target']['chain_id'],
        interaction['target']['res_name'],
        interaction['target']['res_num']
    )
    # weight = interaction['interaction_type']
    weight = 1
    G.add_edge(source_node, target_node, weight=weight)
    source_of_lists.append(source_node)
    target_of_lists.append(target_node)
H = nx.Graph(G)
node_of_set = (set(source_of_lists) | set(target_of_lists))
type(node_of_set)
node_of_list = list(node_of_set)
# Cal the longest path
longest_paths = []
max_length = 0
for i in range(len(node_of_list)-1):
    for j in range(len(node_of_list)-1):
        for path in nx.all_simple_paths(H, node_of_list[i], node_of_list[j]):
            path_length = len(path) - 1
            if path_length > max_length:
                longest_paths = [path]
                max_length = path_length
            elif path_length == max_length:
                longest_paths.append(path)
            j+=1
            print(f"Max path now is {max_length}")
print("############################################")
print("The longest path is:")
print(longest_paths)
print(f"Final Max length is {max_length}")
# All path longer than 10
length_thr = 10
path_thr_list=[]
for i in range(len(node_of_list)-1):
    for j in range(len(node_of_list)-1):
        for path in nx.all_simple_paths(H, node_of_list[i], node_of_list[j]):
            path_length = len(path)
            if path_length >= length_thr:
                path_thr_list.append(path)
            j+=1
print("All paths longer than 10 are:")
print(path_thr_list)
