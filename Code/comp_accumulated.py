import itertools

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from Bachelor.Code.gexf_compare import graph_edit_matrix, comp_name


class MultiComp:
    """
    Class used for creating a custmizable comparison function for
    Graph Edit Distance (from NetworkX)
    """
    def __init__(self, attr_list):
        self.attr_list = attr_list

    def set_attr_list(self, attr_list):
        self.attr_list = attr_list

    def comp_multi_class(self, node1, node2):
        """
        Function that defines if two nodes are considered equal
        (similar to gexf_compare.comp_name).
        Attributes for comparison are given trough class variable 'attr_list'
        :param node1:
        :param node2:
        :return: bool
        """

        if len(self.attr_list) <= 0:
            return True
        for attr in self.attr_list:
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


def accumulated_graph_old(g1, g2, row, col, window):
    """
    Olf function
    :param g1:
    :param g2:
    :param row:
    :param col:
    :param window:
    :return:
    """
    global attr_list
    attr_list = []
    fix_attr = 'Python_name'
    attrs = ['description', 'file_origin', 'recording_date', 'dtype', 'units',
             'shape']
    x_plot = ['Python_name']
    y_plot = [nx.graph_edit_distance(g1, g2, comp_name)]
    for i in range(1, 7):  # num of comparison attributes
        tmp_x = list(itertools.combinations(attrs, i))
        tmp_y = []
        for elem in tmp_x:
            attr_list = ['Python_name'] + list(elem)
            tmp_y.append(nx.graph_edit_distance(g1, g2, comp_multi_gui))

        sorted_l1 = []
        sorted_l2 = []
        sorted_comb = sorted(zip(tmp_y, tmp_x))
        for x, y in sorted_comb:
            sorted_l1.append(x)
            sorted_l2.append(y)
        y_plot.extend(sorted_l1)
        x_plot.extend(sorted_l2)
    x_plot_str = [str(elem) for elem in x_plot]
    # print('accumulated graph labels:', x_plot_str)
    plt.bar(x_plot_str, y_plot)
    plt.ylabel('Graph Edit Distance')
    plt.title(
        "['description', 'file_origin', 'recording_date', 'dtype', 'units', 'shape']")

    indices = [1, 7, 22, 42, 57, 63]
    filtered_labels = [x_plot_str[i] for i in indices]

    plt.xticks(indices, filtered_labels, rotation=10, ha='right', fontsize=6,
               wrap=True)
    plt.ylim(0, max(max(y_plot), 1))
    plt.show()


def accumulated_graph(g1, g2):
    """
    Function that creates a bar plot out of graph edit distance with
    differently sized comparison attribute combinations.
    Every bar ist a combination of the previous bar and one added attribute.
    The added attribute ist chosen by the diffenerce to the previous bar
    by adding this attribute to the comparison.

    :param g1:
    :param g2:
    :return:
    """

    attr_list = []
    comp_obj = MultiComp(attr_list)
    attrs = ['Python_name', 'description', 'file_origin', 'recording_date',
             'dtype', 'units',
             'shape']
    final_x = []
    final_y = []
    for i in range(len(attrs)):  # 1-7
        tmp_x = []
        tmp_y = -1
        for elem in attrs:
            if len(final_x) > 0:
                attr_list = final_x[-1].split(', ')
                attr_list.append(elem)
            else:
                attr_list = [elem]
            comp_obj.set_attr_list(attr_list)
            tmp_ged_res = nx.graph_edit_distance(g1, g2, comp_obj.comp_multi_class)
            if tmp_ged_res > tmp_y:
                tmp_x = list(attr_list)
                tmp_y = tmp_ged_res

        attrs.remove(str(tmp_x[-1]))
        final_x.append(', '.join(tmp_x))
        final_y.append(tmp_y)
    return final_x, final_y

def plot_accumulated_graph(final_x, final_y):
    """
    Creates bar plot from given x and y lists.
    :param final_x:
    :param final_y:
    :return:
    """
    plt.bar(final_x, final_y)
    plt.ylabel('Graph Edit Distance')
    plt.title(
        "['Python_name', 'description', 'file_origin', 'recording_date', 'dtype', 'units', 'shape']")

    plt.xticks(rotation=10, ha='right', fontsize=6, wrap=True)
    plt.ylim(0, max(max(final_y), 1))
    plt.show()


def comp_multi_gui(node1, node2):
    """
    Function that defines if two nodes are considered equal.
    Attributes for comparison are given trough global variable 'attr_list'
    :param node1:
    :param node2:
    :return: bool
    """

    print(attr_list)

    if len(attr_list) <= 0:
        return True
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


def load_graphs_from_gexf(file_paths):
    """
    Loads networkX graph from gexf file
    :param file_paths: string
    :return graphs:
    """

    graph_list = []
    for file in file_paths:
        graph_list.append(nx.read_gexf(file))
    for graph in graph_list:
        graph.remove_edges_from(list(graph.edges()))
    return graph_list


# netx_graph1 = '../Data/comparison_code_graph_new1.gexf'
# # netx_graph1 = '../../gexf_compare/R2G_PSD_all_subjects_simplified.gexf'
# netx_graph2 = '../Data/comparison_code_graph_new4.gexf'
# # netx_graph2 = '../../gexf_compare/R2G_PSD_all_subjects_simplified_Q_units_function.gexf'
# #
# graphs = load_graphs_from_gexf([netx_graph1, netx_graph2])
# x, y = accumulated_graph(graphs[0], graphs[1])
# plot_accumulated_graph(x, y)
