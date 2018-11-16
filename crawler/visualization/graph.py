# coding=utf-8
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

figure_df = pd.read_csv('/Users/chenjunbiao/git/language/gittest/language/language/static/figure_relation.csv')
figure_df = figure_df[0:3000]
source_list = figure_df['0'].tolist()
target_list = figure_df['1'].tolist()
source_list.extend(target_list)
figure_set = set(source_list)
edges = []
for i in range(0, len(figure_df)):
    source = figure_df.iloc[i]['0']
    target = figure_df.iloc[i]['1']
    edges.append((source, target))
G = nx.Graph()
G.add_nodes_from(figure_set)
G.add_edges_from(edges)
nx.draw_networkx(G)
# plt.figure(figsize=(700, 1900))
plt.show()
