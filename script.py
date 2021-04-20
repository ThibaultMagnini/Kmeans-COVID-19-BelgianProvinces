from kmeans import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from util import *
import pandas as pd
import math

kmeans = {}
for i in range(1, 6):
    kmeans[i] = Kmeans('Datasets/temp.csv', i)
    kmeans[i].read_csv(['STANDARD_INFECTION', 'STANDARD_ICU', 'STANDARD_POS_TEST'])
    kmeans[i].start_clustering()

x = []
y = []

print(kmeans[4].accuracy)

for key in kmeans:
    x.append(kmeans[key].k)
    y.append(kmeans[key].accuracy)

plt.plot(x, y)
plt.scatter(x, y)
plt.xlabel("K")
plt.ylabel("Sum of mean squared distances")
plt.title("Elbow graph")
plt.show()

# kmeans[4].draw_scatter_plot_3d()

with open("Results/index.html", "w") as file:
    file.write("")

draw_boxplot(kmeans[1].original_dataset)

for key in kmeans:
    data = []
    for i in range(len(kmeans[key].c)):   
        row = []
        row.append(look_for_province(kmeans[key].original_dataset[i]))
        row.append(round(kmeans[key].c[i]))
        row.append(kmeans[key].original_dataset[i][0])
        row.append(kmeans[key].original_dataset[i][1])
        row.append(kmeans[key].original_dataset[i][2])
        row.append(kmeans[key].original_dataset[i][3])
        data.append(row)

    table = pd.DataFrame(data, columns = ["Province", "Cluster", "Infection rate %", "ICU rate %", "Positive test rate %"])
    table = table.sort_values(by=['Cluster'])
    html = generate_html_table(table)
    
    with open("Results/index.html", "a") as file:
        file.write(f'<h2>K = {key}</h2>')
        file.write(html)