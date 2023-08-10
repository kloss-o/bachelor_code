import argparse
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
from to_dot import ProvenanceGraph
import numpy as np
import time
import random
import pickle

def create_graph(size):
    print(f'creating graph with {size} connections')
    G = nx.Graph()

    #for i in range(size):
    #    G.add_node(i)

    for i in range(size):
        G.add_edge(random.randint(0, size-1), random.randint(0, size-1))

    nx.draw(G)
    #print(G.nodes)
    plt.show()
    return G

#print(nx.graph_edit_distance(create_graph(10), create_graph(10)))

def create_graph_only_nodes(size):
    print(f'creating graph with {size} nodes')
    G = nx.Graph()
    H = nx.Graph()

    for i in range(size):
        G.add_nodes_from([j for j in range(1, i)])
        H.add_nodes_from([k for k in range(int(i/2), int(i + i/2))])

    #for i in range(size):
    #    G.add_edge(random.randint(0, size-1), random.randint(0, size-1))

    #nx.draw_networkx(G)
    #print(G.nodes)
    #plt.show()
    return G, H

#print(nx.graph_edit_distance(create_graph(10), create_graph(10)))

def run_benchmark_edges():

    x = []
    times = []
    difference = []
    for i in range(2, 14, 1):
        x.append(i)
        g1 = create_graph(i)
        g2 = create_graph(i)
        start = time.time()
        #erg = nx.graph_edit_distance(g1, g2)
        for v in nx.optimize_graph_edit_distance(g1, g2):
            minv = v
        runtime = round((time.time()-start)*1000)
        #print(erg)
        difference.append(minv)
        times.append(runtime)

    #plt.plot(x, times)
    #plt.savefig('netx_benchmark.png')
    print(times)
    return times, difference

def run_benchmark_nodes():

    x = []
    times = []
    difference = []
    for i in range(2, 101, 1):
        x.append(i)
        g1, g2 = create_graph_only_nodes(i)
        #g2 = create_graph_only_nodes(i)
        start = time.time()
        #erg = nx.graph_edit_distance(g1, g2)
        for v in nx.optimize_graph_edit_distance(g1, g2):
            minv = v
        runtime = round((time.time()-start)*1000)
        #print(erg)
        difference.append(minv)
        times.append(runtime)

    #plt.plot(x, times)
    #plt.savefig('netx_benchmark.png')
    print(times)
    return times, difference



def benchmark_edges():
    full_times, full_difference = run_benchmark_edges()
    for i in range(19):
        i_times, i_diff = run_benchmark_edges()
        for idx in range(len(full_times)):
            full_times[idx] += i_times[idx]
            full_difference[idx] += i_diff[idx]

    avg_times = [elem / 20 for elem in full_times]
    avg_diff = [elem / 20 for elem in full_difference]

    print(full_times)
    with open('benchmark_data_bigger.pickle', 'wb') as f:
        pickle.dump([avg_times, avg_diff], f)

def benchmark_nodes():
    full_times, full_difference = run_benchmark_nodes()
    for i in range(19):
       i_times, i_diff = run_benchmark_nodes()
       for idx in range(len(full_times)):
           full_times[idx] += i_times[idx]
           full_difference[idx] += i_diff[idx]
    avg_times = [elem / 20 for elem in full_times]
    avg_diff = [elem / 20 for elem in full_difference]
    print(full_times)

    with open('benchmark_data_only_nodes.pickle', 'wb') as f:
       pickle.dump([avg_times, avg_diff], f)

benchmark_nodes()