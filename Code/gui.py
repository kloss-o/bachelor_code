import PySimpleGUI as sg
from text_diff_ import get_text_diff_colormaps
from Bachelor.Code.extract_func import extract_func_list_from_graphs
from Bachelor.Code.func_compare import func_compare_own
from gexf_compare import graph_edit_matrix, load_graphs_from_gexf, comp_name, \
    comp_description, comp_file_origin, comp_recording_date, comp_dtype, \
    comp_units, comp_shape
from comp_accumulated import MultiComp
import networkx as nx
import matplotlib.pyplot as plt
import io
import os

def process_files(file_paths):
    """
    Loads NetworkX Graphs from gexf file and creates GED-Matrix from graphs.
    :param file_paths:
    :return: matrix, graphs
    """
    graphs = load_graphs_from_gexf(file_paths)
    matrix = graph_edit_matrix(graphs)
    return matrix, graphs


def bar_graph(g1, g2, row, col, window_title):
    """
    Creates bar graph of GED with different comparison attributes out
    of two given graphs.

    :param g1:
    :param g2:
    :param row:
    :param col:
    :param window:
    :return: callable
    """
    diff_name = nx.graph_edit_distance(g1, g2, comp_name)
    diff_description = nx.graph_edit_distance(g1, g2, comp_description)
    diff_file_origin = nx.graph_edit_distance(g1, g2, comp_file_origin)
    diff_recording_date = nx.graph_edit_distance(g1, g2, comp_recording_date)
    diff_dtype = nx.graph_edit_distance(g1, g2, comp_dtype)
    diff_units = nx.graph_edit_distance(g1, g2, comp_units)
    diff_shape = nx.graph_edit_distance(g1, g2, comp_shape)

    # plotting
    fig = plt.figure()
    x = ['name', 'description', 'file_origin', 'recording_date', 'dtype',
         'units', 'shape']
    y = [diff_name, diff_description, diff_file_origin, diff_recording_date,
         diff_dtype, diff_units, diff_shape]
    plt.bar(x, y)
    plt.ylabel('Graph Edit Distance')
    plt.xticks(rotation=15, ha='right')
    plt.ylim(0, max(max(y), 1))
    if max(y) <= 0:
        plt.text(3, 0.5, 'Graphs are identical',
                 dict(ha='center', va='center', fontsize=28, color='C1')
                 )

    # show window
    return show_image(fig, window_title)


def accumulated_bar_graph(g1, g2, row, col, window_title):
    """
        Function that creates a bar plot out of graph edit distance with
        differently sized comparison attribute combinations.
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

    # plotting
    fig = plt.figure()
    plt.bar(final_x, final_y)
    plt.ylabel('Graph Edit Distance')

    plt.xticks(rotation=10, ha='right', fontsize=6, wrap=True)
    plt.ylim(0, max(max(final_y), 1))
    if max(final_y) <= 0:
        plt.text(3, 0.5, 'Graphs are identical',
                 dict(ha='center', va='center', fontsize=28, color='C1')
                 )

    # show window
    show_image(fig, window_title)



def create_func_graph_gui(nodes1, nodes2, color_map1, color_map2,
                          window_title):
    """
    Creates function comparison graph out of given nodes and colormaps.
    :param nodes1:
    :param nodes2:
    :param color_map1:
    :param color_map2:
    :param window_title:
    :return: callable
    """
    fig = plt.figure()
    G = nx.Graph()
    labels1 = {}
    for idx in range(len(nodes1) - 1):
        G.add_edge(idx, idx + 1)
    for idx, node in enumerate(G.nodes):
        labels1[node] = str(nodes1[idx]).replace('__main__.', '')
    pos = nx.spring_layout(G, pos={i: (i, 1) for i in G.nodes()},
                           fixed=G.nodes())
    nx.draw_networkx(G, pos=pos, labels=labels1, node_color=color_map1,
            with_labels=True, font_size=10)

    H = nx.Graph()
    labels2 = {}
    for idx in range(len(nodes2) - 1):
        H.add_edge(idx, idx + 1)
    for idx, node in enumerate(H.nodes):
        labels2[node] = str(nodes2[idx]).replace('__main__.', '')
    pos = nx.spring_layout(H, pos={i: (i, 0) for i in H.nodes()},
                           fixed=H.nodes())
    nx.draw_networkx(H, pos=pos, labels=labels2, node_color=color_map2,
            with_labels=True, font_size=10)

    return show_image(fig, window_title)


def func_compare_own_gui(g1, g2):
    """
    Debugging Function?
    :param g1:
    :param g2:
    :return: callable
    """
    nodes1 = extract_func_list_from_graphs(g1)
    nodes2 = extract_func_list_from_graphs(g2)
    color_map1, color_map2 = func_compare_own(nodes1, nodes2)

    return create_func_graph_gui(nodes1, nodes2, color_map1, color_map2)


def show_image(plot, window_title):
    """
    Turns png file to a window object for PySimpleGui.
    :param plot:
    :param window_title:
    :return: image_window
    """
    # convert png to byte stream
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)

    # create PySimpleGUI-Image
    image_elem = sg.Image(data=image_stream.getvalue())
    layout = [[image_elem]]
    image_window = sg.Window(window_title, layout, finalize=True)

    return image_window

def create_graph_windows(graphs, row, col, window, image_windows, file_paths):
    """
    Creates plots of results of diferent methods that compute graph difference
    of the given graphs. Also creates the windows for the plots.
    :param graphs:
    :param row:
    :param col:
    :param window:
    :param image_windows:
    :return:
    """
    # Bar Graph
    image_window = bar_graph(graphs[row], graphs[col], row,
                             col, window_title=f'Einzelvergleich absolut: [{os.path.basename(file_paths[row])}, {os.path.basename(file_paths[col])}]')
    image_windows.append(image_window)

    # own func compare
    graph_1_str = extract_func_list_from_graphs(graphs[row])
    graph_2_str = extract_func_list_from_graphs(graphs[col])
    image_window2 = create_func_graph_gui(graph_1_str,
                                          graph_2_str,
                                          func_compare_own(
                                              graph_1_str,
                                              graph_2_str)[0],
                                          func_compare_own(
                                              graph_1_str,
                                              graph_2_str)[1],
                                          f'func comp: [{os.path.basename(file_paths[row])}, {os.path.basename(file_paths[col])}]')
    image_windows.append(image_window2)

    # Text diff
    image_window3 = create_func_graph_gui(graph_1_str,
                                          graph_2_str,
                                          get_text_diff_colormaps(
                                              graph_1_str,
                                              graph_2_str)[0],
                                          get_text_diff_colormaps(
                                              graph_1_str,
                                              graph_2_str)[1],
                                          f'text diff: [{os.path.basename(file_paths[row])}, {os.path.basename(file_paths[col])}]')
    image_windows.append(image_window3)

    # accumulated bar graph
    image_window4 = accumulated_bar_graph(graphs[row],
                                          graphs[col], row,
                                          col, window_title=f'Einzelvergleich kumuliert: [{os.path.basename(file_paths[row])}, {os.path.basename(file_paths[col])}]')
    image_windows.append(image_window4)

def display_matrix(matrix, window):
    """
    Displays a matrix of Graph Edid Distance results of different graphs.
    :param matrix:
    :param window:
    :return:
    """
    for row in range(len(matrix)):
        buttons_row = []
        for col in range(len(matrix[row])):
            button_key = f"-BUTTON-{row}-{col}-"
            button = sg.Button(f"{matrix[row][col]}", key=button_key)
            buttons_row.append(button)
        window.extend_layout(window, [buttons_row])

def create_frame():
    """
    Creates the overall layout of the gui.
    :return:
    """
    layout = [
        [sg.Text('Wähle Dateien zum Laden aus')],
        [sg.Input(key='-FILES-'), sg.FilesBrowse()],
        [sg.Button('Laden'), sg.Button('Abbrechen')],
        [sg.Text('Ausgewählte Dateien:')],
        [sg.Listbox([], size=(50, 6), key='-FILE_LIST-')],
        [sg.Text('Matrix:')],
    ]

    # create window
    window = sg.Window('Dateien laden', layout)

    return layout, window
def main():
    """
    Runs the gui?
    :return:
    """
    # GUI-Layout
    layout, window = create_frame()

    file_paths = []
    image_windows = []

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Abbrechen':
            break
        elif event == 'Laden':
            selected_files = values['-FILES-'].split(';')
            file_paths.extend(selected_files)
            window['-FILE_LIST-'].update(
                values=file_paths)

            # create matrix
            matrix, graphs = process_files(file_paths)

            # display matrix
            display_matrix(matrix, window)

            # wait on klick
            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED or event == 'Abbrechen':
                    break
                elif event.startswith(
                        "-BUTTON-"):
                    _, row, col, *_ = event.split("-")[
                                      1:]
                    row = int(row)
                    col = int(col)

                    # Create window
                    create_graph_windows(graphs, row, col, window, image_windows, file_paths)

    # close all windows
    for image_window in image_windows:
        image_window.close()

    window.close()


if __name__ == '__main__':
    main()
