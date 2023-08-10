import pickle
import matplotlib.pyplot as plt


with(open('benchmark_data_only_nodes.pickle', 'rb')) as file:
    pickle_input = pickle.load(file)

times = pickle_input[0]
diffs = pickle_input[1]
times_s = [elem/1000 for elem in times]
print(diffs)

time_lists = [[162, 1, 1, 8, 29, 88, 47, 78, 1174, 1604, 12208, 1129],
              [0, 1, 3, 6, 7, 24, 878, 839, 12447, 3889, 4972, 592104],
              [1, 1, 10, 4, 71, 53, 13, 1295, 7469, 90997, 113589, 63837],
              [1, 1, 6, 17, 20, 301, 165, 55, 4390, 50720, 89241, 263760],
              [1, 2, 1, 11, 3, 102, 658, 451, 10450, 5421, 16998, 84204],
              [0, 2, 1, 2, 18, 396, 692, 2212, 295, 1087, 9019, 147087],
              [1, 1, 2, 18, 4, 137, 130, 1327, 14893, 2284, 480502, 218937],
              [0, 2, 1, 7, 61, 62, 307, 623, 5904, 47, 574199, 83375],
              [1, 1, 11, 6, 17, 14, 135, 11029, 17414, 4767, 145859, 191866],
              [1, 2, 1, 6, 3, 32, 3553, 898, 745, 29847, 86305, 318715],
              [0, 1, 9, 25, 26, 20, 80, 4977, 8177, 17722, 24499, 64705],
              [1, 1, 3, 52, 43, 124, 87, 2348, 3291, 41633, 107066, 406296],
              [0, 1, 1, 21, 9, 45, 5, 315, 970, 21028, 430011, 25455],
              [1, 2, 4, 11, 51, 122, 79, 679, 371, 4605, 5997, 181017],
              [0, 1, 1, 17, 72, 72, 431, 776, 15165, 8321, 597231, 1261069]]
kum_time_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for elem in time_lists:
    for i in range(len(elem)):
        kum_time_list[i] += elem[i]

kum_time_list_avg = [elem/1000 for elem in kum_time_list]

plt.plot([i for i in range(2, 101)], times_s)
plt.title('Benchmark für optimize_graph_edit_distance')
plt.ylabel('Laufzeit in s')
plt.xlabel('Anzahl der Knoten im Graphen')
plt.savefig('benchmark_3_times_100_only_nodes.pdf')
plt.show()