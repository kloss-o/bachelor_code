import networkx as nx
from text_diff import text_differences
import copy

from Bachelor.Code.func_compare import create_func_graph, func_compare_own


def convert(graph, erg_list):
    """
    Extracts all nodes that represend function calls from given provenancegraph
     (in NetworkX format).
     If one nodes represents multiple function calls, nodes are duplicated
     so every function call has its own node.
    :param graph:
    :param erg_list:
    :return:
    """
    # print(graph.nodes(data=True))
    for elem1 in list(graph.nodes(data=True)):
        if elem1[1]['type'] == 'function':

            if type(elem1[1]['execution_order']) == str:
                exec_ord = [int(zahl) for zahl in
                            elem1[1]['execution_order'].split(';')]

                for elem in exec_ord:
                    elem2 = copy.deepcopy(elem1)
                    elem2[1]['execution_order'] = elem
                    erg_list.append(elem2)

            else:
                erg_list.append(elem1)


def get_text_diff_colormaps(func_1_strings, func_2_strings):
    """
    Uses text_diff to find equal parts in two lists of nodes.
    Extracts different nodes from string output and creates two colormaps
    which are used to set a color for the nodes in a different NetworkX graph.
    :param func_1_strings:
    :param func_2_strings:
    :return color_map1, color_map2: list, list
    """
    diff = text_differences(func_1_strings, func_2_strings)
    color_map1 = ['grey' for i in range(len(func_1_strings))]
    diff_lines_after_1 = []
    for elem in diff.diff_lines:
        if not str(elem).startswith('Added'):
            diff_lines_after_1.append(elem)
    for idx in range(len(func_1_strings)):
        if str(diff_lines_after_1[idx]).startswith('Modified') or str(
                diff_lines_after_1[idx]).startswith('Removed'):
            color_map1[idx] = 'red'

    diff = text_differences(func_2_strings, func_1_strings)
    color_map2 = ['grey' for i in range(len(func_2_strings))]
    diff_lines_after_2 = []
    for elem in diff.diff_lines:
        if not str(elem).startswith('Added'):
            diff_lines_after_2.append(elem)
    for idx in range(len(func_2_strings)):
        if str(diff_lines_after_2[idx]).startswith('Modified') or str(
                diff_lines_after_2[idx]).startswith('Removed'):
            color_map2[idx] = 'green'

    return color_map1, color_map2


def extract_func_list_from_graphs(graph):
    """
    Extracts function name from list of nodes and converts them to string.
    :param graph:
    :return func_strings: list
    """
    funcs = []
    convert(graph, funcs)
    # print(funcs)   #3, 196, 394, 587
    funcs = sorted(funcs, key=lambda x: x[1]['execution_order'])
    func_strings = []
    for elem in funcs:
        func_strings.append(elem[1]['Python_name'])

    return func_strings


def main():
    file_1 = '../Data/comparison_code_graph_new1.gexf'
    file_2 = '../Data/comparison_code_graph_new4.gexf'
    file_3 = '../../gexf_compare/R2G_PSD_all_subjects.gexf'

    netx_graph1 = nx.read_gexf(file_1)
    netx_graph2 = nx.read_gexf(file_2)
    netx_graph3 = nx.read_gexf(file_3)

    file_1_func = []
    file_2_func = []
    file_3_func = []

    # filter nodes for function executions
    # for elem in [(netx_graph1, file_1_func), (netx_graph2, file_2_func), (netx_graph3, file_3_func)]:
    #    convert(elem[0], elem[1])

    func_1_strings = []
    func_2_strings = []
    func_3_strings = []

    # sorting
    file_1_func = sorted(file_1_func, key=lambda x: x[1]['execution_order'])
    file_2_func = sorted(file_2_func, key=lambda x: x[1]['execution_order'])
    file_3_func = sorted(file_3_func, key=lambda x: x[1]['execution_order'])

    # appending just the name (string for comparison)
    for elem in file_1_func:
        func_1_strings.append(elem[1]['Python_name'])
    for elem in file_2_func:
        func_2_strings.append(elem[1]['Python_name'])
    for elem in file_3_func:
        func_3_strings.append(elem[1]['Python_name'])

    # print(comp1_1(func_1_strings, func_2_strings))

    # create_func_graph(func_1_strings, func_2_strings, get_text_diff_colormaps(func_1_strings, func_2_strings)[0], get_text_diff_colormaps(func_1_strings, func_2_strings)[1])
    # create_func_graph(func_2_strings, func_1_strings, get_text_diff_colormaps(func_2_strings, func_1_strings)[0], get_text_diff_colormaps(func_2_strings, func_1_strings)[1])

    str1 = extract_func_list_from_graphs(netx_graph1)
    str2 = extract_func_list_from_graphs(netx_graph2)
    # str3 = extract_func_list_from_graphs(netx_graph3)

    create_func_graph(str1, str2, func_compare_own(str1, str2)[0],
                      func_compare_own(str1, str2)[1])

    get_text_diff_colormaps(str1, str2)


if __name__ == '__main__':
    main()
