import networkx as nx
import matplotlib.pyplot as plt


def func_compare_own(li1, li2):
    """
    Algorithm that searches for equal parts in two lists of nodes from
    provenance graphs. Looks through every element of both lists and searches
    for equal sections. Is an equal section ist found, the elements of the
    section are saved for a plotting function.

    :param li1:
    :param li2:
    :return color_map1, color_map2: list, list
    """
    right_1 = []
    right_2 = []

    unsure_1 = []
    unsure_2 = []

    wrong_1 = []
    wrong_2 = []

    color_map1 = ['green' for i in range(len(li1))]
    color_map2 = ['green' for i in range(len(li2))]

    i, j = 0, 0
    while i < len(li1) and j < len(li2):
        if li1[i] == li2[j]:
            # print(li1[i], li2[j])
            right_1.append(i)
            right_2.append(j)
            color_map1[i] = 'grey'
            color_map2[j] = 'grey'
            i += 1
            j += 1
        else:
            if li1[i] in li2[j:] and li2[j] in li1[i:]:
                # Searches closest appearence
                first_elem_in_sec_list = li2[j + 1:].index(li1[i]) + 1
                sec_elem_in_first_list = li1[i + 1:].index(li2[j]) + 1

                if first_elem_in_sec_list < sec_elem_in_first_list:
                    # color_map2[j] = 'green'
                    wrong_2.append(j)
                    j += 1
                elif sec_elem_in_first_list < first_elem_in_sec_list:
                    # color_map1[i] = 'green'
                    wrong_1.append(i)
                    i += 1
                elif first_elem_in_sec_list == sec_elem_in_first_list:
                    color_map1[i] = 'orange'
                    unsure_1.append(i)
                    color_map2[j] = 'orange'
                    unsure_2.append(j)
                    i += 1
                    j += 1
                else:
                    raise IndexError

            elif li1[i] in li2[j:] and li2[j] not in li1[i:]:
                # color_map2[j] = 'green'
                wrong_2.append(j)
                j += 1
            elif li1[i] not in li2[j:] and li2[j] in li1[i:]:
                # color_map1[i] = 'green'
                wrong_1.append(i)
                i += 1
            elif li1[i] not in li2[j:] and li2[j] not in li1[i:]:
                color_map1[i] = 'orange'
                unsure_1.append(i)
                color_map2[j] = 'orange'
                unsure_2.append(j)
                i += 1
                j += 1
            else:
                raise IndexError
    if i >= len(li1) and j >= len(li2):
        # return wrong_1, wrong_2, unsure_1, unsure_2
        return color_map1, color_map2
    elif i >= len(li1) and j < len(li2):
        wrong_2 += range(j, len(li2))
        # return wrong_1, wrong_2, unsure_1, unsure_2
        return color_map1, color_map2
    elif i < len(li1) and j >= len(li2):
        wrong_1 += range(i, len(li1))
        # return wrong_1, wrong_2, unsure_1, unsure_2
        return color_map1, color_map2
    else:
        raise IndexError


def create_func_graph(nodes1, nodes2, color_map1, color_map2):
    """
    Creates a networkX graph from two lists of nodes and two colormaps.
    :param nodes1:
    :param nodes2:
    :param color_map1:
    :param color_map2:
    :return:
    """

    G = nx.Graph()
    labels1 = {}
    for idx in range(len(nodes1) - 1):
        G.add_edge(idx, idx + 1)
    for idx, node in enumerate(G.nodes):
        labels1[node] = str(nodes1[idx]).replace('__main__.', '')
    pos = nx.spring_layout(G, pos={i: (i, 1) for i in G.nodes()},
                           fixed=G.nodes())
    nx.draw(G, pos=pos, labels=labels1, node_color=color_map1,
            with_labels=True)

    H = nx.Graph()
    labels2 = {}
    for idx in range(len(nodes2) - 1):
        H.add_edge(idx, idx + 1)
    for idx, node in enumerate(H.nodes):
        labels2[node] = str(nodes2[idx]).replace('__main__.', '')
    pos = nx.spring_layout(H, pos={i: (i, 0) for i in H.nodes()},
                           fixed=H.nodes())
    nx.draw(H, pos=pos, labels=labels2, node_color=color_map2,
            with_labels=True)
    plt.show()


def main():
    """
    only for testing data
    """

    # notes
    a = [1, 2, 4, 5, 8]
    b = [1, 2, 3, 4, 8]

    # paper
    c = [1, 2, 4, 5, 7, 8, 9, 7, 9, 4]
    d = [1, 2, 3, 4, 5, 7, 8, 7, 9, 9, 4]

    # random
    e = [9, 2, 5, 7, 3, 9, 2, 4, 6, 1]
    f = [8, 3, 6, 1, 4, 8, 9, 2, 4, 5]

    # print(comp1_1(c, d))
    # print(comp1_1(b, a))

    create_func_graph(c, d, func_compare_own(c, d)[0],
                      func_compare_own(c, d)[1])


if __name__ == '__main__':
    main()
