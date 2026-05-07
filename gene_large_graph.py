import networkx as nx
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os


def refine_dag(graph, min_subnodes=5, max_subnodes=10):
    """
    将DAG图graph细化为更详细的DAG图large_graph
    
    参数:
    graph: 原始DAG图
    min_subnodes: 每个节点最少细化为多少个子节点
    max_subnodes: 每个节点最多细化为多少个子节点
    
    返回:
    large_graph: 细化后的DAG图
    node_mapping: 原始节点到细化节点列表的映射
    """
    
    # 创建新的DAG图large_graph
    large_graph = nx.DiGraph()
    
    # 存储原始节点到细化节点的映射
    node_mapping = {}
    
    # 第一步：为graph中的每个节点创建细化的子节点
    for node in graph.nodes():
        # 随机确定该节点需要细化为多少个子节点
        num_subnodes = random.randint(min_subnodes, max_subnodes)
        
        # 创建细化的子节点
        subnodes = []
        for i in range(1,num_subnodes+1):
            # 为子节点创建唯一标识符
            subnode_id = node[:4] + str(i) if i>=10 else node[:4] + '0' + str(i)
            subnodes.append(subnode_id)
            large_graph.add_node(subnode_id, original_node=node)
        
        # 保存映射关系
        node_mapping[node] = subnodes
        
        # 第二步：在细化的子节点内部创建连接关系
        # 创建复杂的内部连接（树状结构）
        for i in range(1, len(subnodes)):
            # 每个子节点连接到之前的一个随机节点
            parent_idx = random.randint(0, i-1)
            large_graph.add_edge(subnodes[parent_idx], subnodes[i])
    
    # 第三步：根据graph中的边关系，在large_graph中创建对应的子节点间连接
    for edge in graph.edges():
        source_node, target_node = edge
        
        # 获取对应的细化节点列表
        source_subnodes = node_mapping[source_node]
        target_subnodes = node_mapping[target_node]
        
        # 在源节点的最后一个子节点和目标节点的第一个子节点之间创建连接
        # 这样可以保持DAG性质
        large_graph.add_edge(source_subnodes[-1], target_subnodes[0])
        
        # 可选：添加一些额外的连接以增加复杂性
        # 随机添加一些跨层连接（确保不破坏DAG性质）
        if random.random() < 0.3:  # 30%概率添加额外连接
            random_source = random.choice(source_subnodes[:-1])  # 不选择最后一个
            random_target = random.choice(target_subnodes[1:])   # 不选择第一个
            # 检查添加这条边是否会形成环
            large_graph_test = large_graph.copy()
            large_graph_test.add_edge(random_source, random_target)
            if nx.is_directed_acyclic_graph(large_graph_test):
                large_graph.add_edge(random_source, random_target)
    
    return large_graph, node_mapping

graph = nx.DiGraph()

# 读取节点和边数据
node_df = pd.read_excel('data/nodelist_detailed.xlsx', dtype={'id': str})  # id列为 'id'
edge_df = pd.read_excel('data/edgelist_detailed.xlsx', dtype={'source': str, 'target': str})  #  'source' 和 'target'列为str

# 添加节点
for index, row in node_df.iterrows():
    node_id = row['id']
    node_label = row['label']
    graph.add_node(node_id)
    graph.nodes[node_id]['label'] = node_label
    graph.nodes[node_id]['time'] = row['time']
    graph.nodes[node_id]['cost'] = row['cost']
    graph.nodes[node_id]['status'] = 1  # 初始化状态为1，表示未执行

# 添加边
for index, row in edge_df.iterrows():
    source = row['source']
    target = row['target']
    # if '0000' not in source and '0000' not in target:
    relation_attr = row['relation']
    graph.add_edge(source, target)
    graph[source][target]['relation'] = relation_attr
print('节点数：', len(graph.nodes))
print('边数：', len(graph.edges))

large_graph, node_mapping = refine_dag(graph)
plt.figure(figsize=(10, 8))
nx.draw(large_graph, with_labels=True, node_color='lightblue', node_size=800, font_size=12)
# plt.show()
print('节点数：', len(large_graph.nodes))
print('边数：', len(large_graph.edges))
# 检查图是否包含环
if nx.is_directed_acyclic_graph(large_graph):
    print("图是DAG图")
else:
    print("图不是DAG图")

# 节点数据
node_list = [{'id': node} for node in large_graph.nodes()]
node_df = pd.DataFrame(node_list)
node_df.to_excel('data/nodelist_large.xlsx', index=False)

# 连边数据
edge_list = [{'source': edge[0], 'target': edge[1]} for edge in large_graph.edges()]
edge_df = pd.DataFrame(edge_list)
edge_df.to_excel('data/edgelist_large.xlsx', index=False)