import pandas as pd
import networkx as nx

# 读取表格数据
df = pd.read_csv('interactions.csv')

# 解析相互作用信息
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

# 构建相互作用网络
G = nx.DiGraph()

for interaction in interactions:
    # 使用相互作用起点和终点的氨基酸序号作为节点
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
    
    # 将相互作用的类型作为边的权重
    weight = interaction['interaction_type']
    
    G.add_edge(source_node, target_node, weight=weight)

# 查找最短路径
shortest_path = nx.shortest_path(G, source='A:THR:44', target='D:CYS:157')

print(shortest_path)
