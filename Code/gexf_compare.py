import argparse
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from to_dot import ProvenanceGraph
import numpy as np
import time


def load_graphs_from_gexf(file_paths):
    """
    Loads networkX graph from gexf file.
    :param file_paths: string
    :return graphs: NetworkX graph object
    """

    graphs = []
    for file in file_paths:
        graphs.append(nx.read_gexf(file))
    for graph in graphs:
        graph.remove_edges_from(list(graph.edges()))
    return graphs


def graph_edit_matrix(graphs):
    """
    Creates matrix of Graph Edit Distance (from NetworkX) between graphs.
    :param graphs:
    :return matrix:
    """

    result = [[0.0 for j in range(len(graphs))] for i in
              range(len(graphs))]

    for i in range(len(graphs)):
        for j in range(i+1, len(graphs)):
            result[i][j] = nx.graph_edit_distance(graphs[i], graphs[j], comp_name)
            result[j][i] = result[i][j]

    return result


# Comparing functions used to use as parameters for graph edit distance from
# here
def comp_name(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attribute for comparison is 'Python_name'.
    Function searches for the given attribute in both nodes.
    If both nodes have the attribute and they are equal or
    both nodes don't have the attribute, the node is considered equal.
    Otherwise they are considered as not equal.

    :param node1: NetworkX object
    :param node2: NetworkX object
    :return: bool
    """

    try:
        # print(node1['name'], node2['name'], node1['name'] == node2['name'])
        if 'Python_name' not in node1 and 'Python_name' not in node2:
            return True
        elif ('Python_name' not in node1) ^ ('Python_name' not in node2):
            return False
        elif node1['Python_name'] == node2['Python_name']:
            return True
        else:
            return False
    except:
        return False


def comp_description(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attribute for comparison is 'description'.
    Function searches for the given attribute in both nodes.
    If both nodes have the attribute and they are equal or
    both nodes don't have the attribute, the node is considered equal.
    Otherwise they are considered as not equal.

    :param node1: NetworkX object
    :param node2: NetworkX object
    :return: bool
    """

    try:
        if 'description' not in node1 and 'description' not in node2:
            return True
        elif ('description' not in node1) ^ ('description' not in node2):
            return False
        elif node1['description'] == node2['description']:
            return True
        else:
            return False
    except:
        return False


def comp_file_origin(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attribute for comparison is 'file_origin'.
    Function searches for the given attribute in both nodes.
    If both nodes have the attribute and they are equal or
    both nodes don't have the attribute, the node is considered equal.
    Otherwise they are considered as not equal.

    :param node1: NetworkX object
    :param node2: NetworkX object
    :return: bool
    """

    try:
        if 'file_origin' not in node1 and 'file_origin' not in node2:
            return True
        elif ('file_origin' not in node1) ^ ('file_origin' not in node2):
            return False
        elif node1['file_origin'] == node2['file_origin']:
            return True
        else:
            return False
    except:
        return False


def comp_recording_date(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attribute for comparison is 'recording_date'.
    Function searches for the given attribute in both nodes.
    If both nodes have the attribute and they are equal or
    both nodes don't have the attribute, the node is considered equal.
    Otherwise they are considered as not equal.

    :param node1: NetworkX object
    :param node2: NetworkX object
    :return: bool
    """

    try:
        if 'recording_date' not in node1 and 'recording_date' not in node2:
            return True
        elif ('recording_date' not in node1) ^ ('recording_date' not in node2):
            return False
        elif node1['recording_date'] == node2['recording_date']:
            return True
        else:
            return False
    except:
        return False


def comp_dtype(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attribute for comparison is 'dtype'.
    Function searches for the given attribute in both nodes.
    If both nodes have the attribute and they are equal or
    both nodes don't have the attribute, the node is considered equal.
    Otherwise they are considered as not equal.

    :param node1: NetworkX object
    :param node2: NetworkX object
    :return: bool
    """

    try:
        if 'dtype' not in node1 and 'dtype' not in node2:
            return True
        elif ('dtype' not in node1) ^ ('dtype' not in node2):
            return False
        elif node1['dtype'] == node2['dtype']:
            return True
        else:
            return False
    except:
        return False


def comp_units(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attribute for comparison is 'units'.
    Function searches for the given attribute in both nodes.
    If both nodes have the attribute and they are equal or
    both nodes don't have the attribute, the node is considered equal.
    Otherwise they are considered as not equal.

    :param node1: NetworkX object
    :param node2: NetworkX object
    :return: bool
    """

    try:
        if 'units' not in node1 and 'units' not in node2:
            return True
        elif ('units' not in node1) ^ ('units' not in node2):
            return False
        elif node1['units'] == node2['units']:
            return True
        else:
            return False
    except:
        return False


def comp_shape(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attribute for comparison is 'shape'.
    Function searches for the given attribute in both nodes.
    If both nodes have the attribute and they are equal or
    both nodes don't have the attribute, the node is considered equal.
    Otherwise they are considered as not equal.

    :param node1: NetworkX object
    :param node2: NetworkX object
    :return: bool
    """

    try:
        if 'shape' not in node1 and 'shape' not in node2:
            return True
        elif ('shape' not in node1) ^ ('shape' not in node2):
            return False
        elif node1['shape'] == node2['shape']:
            return True
        else:
            return False
    except:
        return False


def comp_multi(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attributes for comparison are given trough global variable 'attr_list'
    :param node1:
    :param node2:
    :return: bool
    """

    for attr in attr_list:
        try:
            if attr not in node1 and attr not in node2:
                continue
            elif (attr not in node1) ^ (attr not in node2):
                return False
            elif node1[attr] == node2[attr]:
                continue
            else:
                return False
        except:
            return False

    return True


def create_test_graph_old(type):
    if type == 1:
        G = nx.Graph()
        G.add_node(1, Python_name='exp1', val=6)
        G.add_node(2, Python_name='exp3', val=4)
        G.add_node(3, Python_name='exp2', val=6)
        # G.add_node(4, name='exp1', val=7)
        # G.add_edge(1, 2)
        # G.add_edge(1, 3)
        # G.add_edge(1, 5)
        # G.add_edge(2, 3)
        # G.add_edge(3, 4)
        # G.add_edge(4, 5)
        # nx.draw_networkx(G)
        return G

    elif type == 2:
        H = nx.Graph()
        H.add_node(1, Python_name='exp1', val=6)
        H.add_node(2, Python_name='exp1', val=6)
        H.add_node(3, Python_name='exp4', val=6)
        # H.add_edge(1, 2)
        H.add_edge(1, 3)
        # H.add_edge(2, 3)
        # H.add_edge(3, 4)
        # H.add_edge(3, 5)
        # H.add_edge(5, 6)

        # nx.draw_networkx(H)
        return H
    else:
        return -1


def test_compare():
    # nx.draw(netx_graph1, with_labels=True)
    # nx.draw(netx_graph2, with_labels=False)

    # difference
    # netx_graph_diff1 = nx.difference(netx_graph1, netx_graph2)
    # netx_graph_diff2 = nx.difference(netx_graph2, netx_graph1)
    # netx_graph_diff3 = nx.difference(netx_graph1, netx_graph1)
    # nx.draw(netx_graph_diff3)

    # netx_graph_diff1_1 = nx.from_edgelist(netx_graph1.edges() - netx_graph2.edges())
    # netx_graph_diff2_1 = nx.from_edgelist(netx_graph2.edges() - netx_graph1.edges())
    # nx.draw(netx_graph_diff1_1, with_labels=True)
    # nx.draw(netx_graph_diff2_1, with_labels=False)

    # isomorph
    # print('is_isomorphic(g1, g2):', nx.is_isomorphic(netx_graph1, netx_graph2))
    # print('is_isomorphic(g1, g1):', nx.is_isomorphic(netx_graph1, netx_graph1), '\n')

    # graph_equal
    # print('is_equal(g1, g2):', nx.utils.graphs_equal(netx_graph1, netx_graph2))
    # print('is_equal(g1, g1):', nx.utils.graphs_equal(netx_graph1, netx_graph1), '\n')
    pass


def main():
    # G = create_test_graph_old(1)
    # H = create_test_graph_old(2)

    # difference (node sets net equal)
    # netx_graph_diff1 = nx.difference(G, H)
    # netx_graph_diff2 = nx.difference(G, H)
    # netx_graph_diff3 = nx.difference(G, G)
    # nx.draw(netx_graph_diff3)

    # netx_graph_diff1_1 = nx.from_edgelist(G.edges() - H.edges())
    # netx_graph_diff2_1 = nx.from_edgelist(H.edges() - G.edges())
    # nx.draw(netx_graph_diff1_1, with_labels=True)
    # nx.draw(netx_graph_diff2_1, with_labels=True)

    # isomorph
    # print('is_isomorphic(g1, g2):', nx.is_isomorphic(G, H))
    # print('is_isomorphic(g1, g1):', nx.is_isomorphic(G, G), '\n')

    # graph_equal
    # print('is_equal(g1, g2):', nx.utils.graphs_equal(G, H))
    # print('is_equal(g1, g1):', nx.utils.graphs_equal(G, G))

    # similarity measures
    # netx_graph1 = '../../gexf_compare/R2G_PSD_all_subjects.gexf'
    # netx_graph2 = '../Data/comparison_code_graph_new2.gexf'
    # global attr_list
    # attr_list = []
    # print('graph_edit_distance:\n', np.matrix(graph_edit_array(load_graphs_from_gexf([netx_graph1, netx_graph2]))))

    # print(G.edges)
    # print(H.edges)
    # print(nx.graph_edit_distance(G, H, comp_name, comp_edge))
    # print(nx.graph_edit_distance(H, G, comp_name, comp_edge))
    # print('my:', list_comp_diff(list(netx_graph3.nodes(data=True)), list(netx_graph4.nodes(data=True))))
    # print(nx.graph_edit_distance(G, H, comp_val))
    # print(nx.graph_edit_distance(H, G, comp_val))
    # print(list_comp_diff(list(netx_graph1.nodes(data=True)), list(netx_graph2.nodes(data=True))))

    # print(nx.graph_edit_distance(netx_graph3, netx_graph3, comp_name))
    # print(nx.graph_edit_distance(netx_graph4, netx_graph3, comp_name))

    # graphs = load_graphs_from_gexf(['../../gexf_compare/R2G_PSD_all_subjects_simplified.gexf', '../../gexf_compare/R2G_PSD_all_subjects_simplified_Q_units_function.gexf'])
    # matrix = graph_edit_array(graphs)
    # print(matrix)
    # #plt.plot(matrix)
    pass


if __name__ == "__main__":
    # main()
    plt.show()
