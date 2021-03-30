from kmeans import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from util import *
import pandas as pd
import math


"""kmeans3 = Kmeans('Datasets/output.csv', 3)
kmeans3.read_csv(['INFECTION_RATE', 'TEST_POS_PERCENTAGE'])
kmeans3.start_clustering()
print(kmeans3.c)"""


""" ax = plt.axes(projection='3d')
for cluster in range(kmeans3.k):
    elements_x = []
    elements_y = []
    elements_z = []
    elements = np.where(kmeans3.c == cluster)
    element_cluster = np.array(kmeans3.original_dataset)[elements[0]]
    for element in element_cluster:
        elements_x.append(element[0])
        elements_y.append(element[1])
        elements_z.append(element[2])
    ax.scatter3D(elements_x, elements_y, elements_z, c=elements_z, cmap='Greens')
plt.show() """

kmeans = {}
for i in range(1, 6):
    kmeans[i] = Kmeans('Datasets/output.csv', i)
    kmeans[i].read_csv(['INFECTION_RATE', 'ICU_RATE','UNEMPLOYEMENT_RATE', 'TEST_POS_PERCENTAGE'])
    print(kmeans[i].original_dataset)
    kmeans[i].start_clustering()


x = []
y = []

"""
for key in kmeans:
    plt.subplot(3, 2, key)
    plt.subplots_adjust(hspace=0.35)
    plt.title(f"K = {key}")
    kmeans[key].draw_scatter_plot('INFECTIONS', 'AMOUNT OF TESTS (in millions)', [0, 200000], [0, 2000000], False)
    x.append(kmeans[key].k)
    y.append(kmeans[key].accuracy)
plt.subplot(3, 2, 6)
plt.plot(x, y)
plt.scatter(x, y)
plt.title("Elbow graph")"""

with open("Results/index.html", "w") as file:
    file.write("")

for key in kmeans:
    data = []
    # draw_boxplot(kmeans[key].original_dataset)
    for i in range(len(kmeans[key].c)):   
        row = []
        row.append(look_for_province(kmeans[key].original_dataset[i]))
        row.append(round(kmeans[key].c[i]))
        row.append(kmeans[key].original_dataset[i][0])
        row.append(kmeans[key].original_dataset[i][1])
        row.append(kmeans[key].original_dataset[i][2])
        row.append(kmeans[key].original_dataset[i][3])
        data.append(row)

    table = pd.DataFrame(data, columns = ["Province", "Cluster", "Infection rate %", "ICU rate %", "Unemployment rate %", "Positive test rate %"])
    table = table.sort_values(by=['Cluster'])
    html = generate_html_table(table)
    
    with open("Results/index.html", "a") as file:
        file.write(f'<h2>K = {key}</h2>')
        file.write(html)

plt.show()