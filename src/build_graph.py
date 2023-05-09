import glob
import itertools
import json
import os
import random
import pandas
from communities.algorithms import girvan_newman, louvain_method
from communities.visualization import draw_communities
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import community


def edge_dist(edge):
    # dist = edge['uv_vote_dist'] + 999   # 众议院的边权
    dist = edge['uv_cosponsor']     # 参议院的边权
    return dist


def build_graph(node_dir, edge_dir, conf):
    c = '1161'
    all_nodes = dict()
    idx2id = dict()
    node_pth = os.path.join(node_dir, c + '.csv')
    nodes = pandas.read_csv(node_pth, header=None)
    edge_pth = os.path.join(edge_dir, 'uv' + c + '.csv')
    edges = pandas.read_csv(edge_pth, header=None)
    size = 0
    for p in range(len(nodes)):
        if nodes.iloc[p, 0] not in all_nodes.keys():
            node_dict = {
                'id': size,
                'party': nodes.iloc[p, 1],
                'name': nodes.iloc[p, 2],
                'state': nodes.iloc[p, 3],
                'career': nodes.iloc[p, 4],
                'sponsor': int(nodes.iloc[p, 5]),
                'cosponsor': int(nodes.iloc[p, 6]),
            }
            all_nodes[nodes.iloc[p, 0]] = node_dict
            idx2id[size] = nodes.iloc[p, 0]
            size += 1

    adj_matrix = np.zeros((size, size), dtype=float)

    for e in range(len(edges)):
        edge_dict = {
            'u_node': edges.iloc[e, 0],
            'v_node': edges.iloc[e, 1],
            'u_lead_v': edges.iloc[e, 2],
            'v_lead_u': edges.iloc[e, 3],
            'uv_cosponsor': edges.iloc[e, 4],
            'u_votes': edges.iloc[e, 5],
            'v_votes': edges.iloc[e, 6],
            'uv_votes': edges.iloc[e, 7],
            'uv_vote_dist': edges.iloc[e, 8],
            'uv_a_no': edges.iloc[e, 9],
            'uv_b_no': edges.iloc[e, 11],
            'uv_c_no': edges.iloc[e, 13],
            'uv_d_no': edges.iloc[e, 15],
            'uv_e_no': edges.iloc[e, 17],
            'uv_f_no': edges.iloc[e, 19],
            'uv_g_no': edges.iloc[e, 21],
            'uv_h_no': edges.iloc[e, 23],
            'uv_a_dist': edges.iloc[e, 10],
            'uv_b_dist': edges.iloc[e, 12],
            'uv_c_dist': edges.iloc[e, 14],
            'uv_d_dist': edges.iloc[e, 16],
            'uv_e_dist': edges.iloc[e, 18],
            'uv_f_dist': edges.iloc[e, 20],
            'uv_g_dist': edges.iloc[e, 22],
            'uv_h_dist': edges.iloc[e, 24],
        }
        idu = all_nodes[edges.iloc[e, 0]]['id']
        idv = all_nodes[edges.iloc[e, 1]]['id']

        adj_matrix[idu, idv] = adj_matrix[idv, idu] = edge_dist(edge_dict)

    return adj_matrix, all_nodes, idx2id


if __name__ == '__main__':
    # vote_path = '.\\data\\vote\\votes.json'
    # with open(vote_path) as f:
    #     vote = json.load(f)
    #     print(len(vote))
    #     print(vote[0:100])
    #
    # exit(0)
    node_path = '.\\data\\node\\*.csv'
    node_dir = '.\\data\\node'
    edge_path = '.\\data\\edge\\*.csv'
    edge_dir = '.\\data\\edge'
    node_files = glob.glob(node_path)
    conf = []
    for nf in node_files:
        conf.append(os.path.basename(nf).split('.')[0])

    ratio = 0.8
    section = int(ratio * len(conf))
    random.seed(1234)
    # random.shuffle(conf)

    train = conf[:section]
    test = conf[section:]

    ### save graph
    # adj_mat, all_nodes, idx2id = build_graph(node_dir, edge_dir, train)
    # np.savez('adj_mat.npz', adj_mat)
    # with open('idx2id.json', 'w') as f:
    #     json.dump(idx2id, f)
    # with open('all_nodes.json', 'w') as f:
    #     json.dump(all_nodes, f)


    ### read graph
    adj_matrix = np.load('adj_mat.npz')['arr_0']
    with open('idx2id.json') as f:
        idx2id = json.load(f)
    with open('all_nodes.json') as f:
        all_nodes = json.load(f)

    g = nx.Graph()
    size = len(idx2id)
    print(size)

    for i in range(size):
        for j in range(size):
            if adj_matrix[i, j] > 0:
                g.add_edge(i, j, weight=adj_matrix[i, j])

    node_weight = dict()
    for i in range(size):
        if i not in g.nodes():
            g.add_node(i)

        weight = 0
        for u, v, w in g.edges().data('weight'):
            if u == i:
                weight += w

        node_weight[i] = weight


    # democrats = [all_nodes[idx2id[str(u)]]['name'] for u in g.nodes() if all_nodes[idx2id[str(u)]]['party'] == 'Democratic']
    # republicans = [all_nodes[idx2id[str(u)]]['name'] for u in g.nodes() if all_nodes[idx2id[str(u)]]['party'] == 'Republican']
    democrats = [u for u in g.nodes() if all_nodes[idx2id[str(u)]]['party'] == 'Republican']
    # republicans = [u for u in g.nodes() if all_nodes[idx2id[str(u)]]['party'] == 'Republican']
    partition = community.community_louvain.best_partition(g, randomize=False, resolution=1)
    group_no = np.max(list(partition.values()))
    d_group = dict()
    # r_group = dict()
    for no in range(group_no+1):
        d_group[no] = [all_nodes[idx2id[str(node)]]['name'] for node in democrats if partition.get(node) == no]
        if len(d_group[no])>1:
            print('d_%d: ' % no, d_group[no])
        # r_group[no] = [all_nodes[idx2id[str(node)]]['name'] for node in republicans if partition.get(node) == no]
        # print('r_%d: ' % no, r_group[no])
    size = float(len(set(partition.values())))

    d_vals = [partition.get(node) + 5 for node in democrats]
    # r_vals = [partition.get(node) for node in republicans]

    d_size = [(node_weight[node] / 50) ** 3 + 100 for node in democrats]
    d_label = {node: all_nodes[idx2id[str(node)]]['name'] for node in democrats}
    # values = [partition.get(node) for node in g.nodes()]
    pos = nx.shell_layout(g)
    plt.figure(figsize=(10, 10), dpi=100)
    nx.draw_networkx_nodes(
        g, pos, democrats,
        cmap=plt.get_cmap('jet'),
        node_color=d_vals,
        node_size=d_size,
        node_shape='o',
        edgecolors='white'
    )
    nx.draw_networkx_labels(g, pos, d_label, font_size=8)

    # d_edges = [(u, v) for (u, v) in g.edges() if u in democrats and v in democrats]
    thresh = 0
    d_edges = [(u, v) for (u, v, w) in g.edges.data('weight') if u in democrats and v in democrats and w >= thresh]
    d_edge_width = [(w/25) ** 5 + 0.05 for (u, v, w) in g.edges.data('weight') if u in democrats and v in democrats and w >= thresh]

    nx.draw_networkx_edges(g, pos, d_edges, d_edge_width)
    plt.show()
    # plt.subplot(121)
    # plt.title('Democrats', size=32)
    # nx.draw_networkx_nodes(
    #     g, pos, democrats, cmap=plt.get_cmap('jet'), node_color=d_vals, node_size=100, node_shape='o')
    # plt.subplot(122)
    # plt.title('Republicans', size=32)
    # nx.draw_networkx_nodes(
    #     g, pos, republicans, cmap=plt.get_cmap('jet'), node_color=r_vals, node_size=100, node_shape='o')
    # # nx.draw_random(g, cmap=plt.get_cmap('jet'), node_color=values, node_size=30, with_labels=False)
    # plt.show()
