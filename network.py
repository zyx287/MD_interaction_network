import pandas as pd
import networkx as nx

df = pd.read_csv('interactions.csv')

interactions = []
for row in df:
    parts = row.split('\t')
    frame = int(parts[0])
    interaction_type = parts[1]
    source = parts[2]
    target = parts[3]
    
    source_parts = source.split(':')
    source_chain_id = source_parts[0]
    source_res_name = source_parts[1]
    source_res_num = int(source_parts[2])
    source_atom_name = source_parts[3]
    source_data = {
        'chain_id': source_chain_id,
        'res_name': source_res_name,
        'res_num': source_res_num,
        'atom_name': source_atom_name
    }
    
    target_parts = target.split(':')
    target_chain_id = target_parts[0]
    target_res_name = target_parts[1]
    target_res_num = int(target_parts[2])
    target_atom_name = target_parts[3]
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
    
    weight = interaction['interaction_type']
    
    G.add_edge(source_node, target_node, weight=weight)

shortest_path = nx.shortest_path(G, source='A:THR:44', target='D:CYS:157')

print(shortest_path)
