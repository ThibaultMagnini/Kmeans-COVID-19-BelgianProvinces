from kmeans import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from util import *
import pandas as pd
import math

kmeans = {}
for i in range(1, 6):
    kmeans[i] = Kmeans('Datasets/output.csv', i)
    kmeans[i].read_csv(['INFECTION_RATE', 'ICU_RATE', 'TEST_POS_PERCENTAGE'])
    print(kmeans[i].get_dataset_info())
    kmeans[i].start_clustering()

x = []
y = []

for key in kmeans:
    x.append(kmeans[key].k)
    y.append(kmeans[key].accuracy)
plt.plot(x, y)
plt.scatter(x, y)
plt.xlabel("K")
plt.ylabel("Sum of mean squared distances")
plt.title("Elbow graph")
plt.show()

ax = plt.axes(projection='3d')
ax.set_xlabel('Infection Rate (%)')
ax.set_ylabel('ICU Rate (%)')
ax.set_zlabel('Positive tests (%)')
colors = ["red", "green", "cyan", "purple", "yellow", "blue"]

rep_x = []
rep_y = []
rep_z = []

for cluster in range(kmeans[4].k):
    elements_x = []
    elements_y = []
    elements_z = []
    elements = np.where(kmeans[4].c == cluster)
    element_cluster = np.array(kmeans[4].original_dataset)[elements[0]]
    for element in element_cluster:
        elements_x.append(element[0])
        elements_y.append(element[1])
        elements_z.append(element[2])
        ax.plot([element[0], kmeans[4].representatives[cluster][0]], [element[1], kmeans[4].representatives[cluster][1]], [element[2], kmeans[4].representatives[cluster][2]], c=colors[cluster])
    ax.scatter3D(elements_x, elements_y, elements_z, c=colors[cluster], label=f"Cluster {cluster + 1}", alpha=1)
    rep_x.append(kmeans[4].representatives[cluster][0])
    rep_y.append(kmeans[4].representatives[cluster][1])
    rep_z.append(kmeans[4].representatives[cluster][2])
ax.scatter3D(rep_x, rep_y, rep_z, c="black", label="Representatives", alpha=1)
ax.legend()
plt.show()

with open("Results/index.html", "w") as file:
    file.write("")

for key in kmeans:
    data = []
    draw_boxplot(kmeans[key].original_dataset)
    for i in range(len(kmeans[key].c)):   
        row = []
        row.append(look_for_province(kmeans[key].original_dataset[i]))
        row.append(round(kmeans[key].c[i]))
        row.append(kmeans[key].original_dataset[i][0])
        row.append(kmeans[key].original_dataset[i][1])
        row.append(kmeans[key].original_dataset[i][2])
        data.append(row)

    table = pd.DataFrame(data, columns = ["Province", "Cluster", "Infection rate %", "ICU rate %", "Positive test rate %"])
    table = table.sort_values(by=['Cluster'])
    html = generate_html_table(table)
    
    with open("Results/index.html", "a") as file:
        file.write(f'<h2>K = {key}</h2>')
        file.write(html)