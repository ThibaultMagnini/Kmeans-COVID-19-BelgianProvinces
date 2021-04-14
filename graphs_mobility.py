import matplotlib.pyplot as plt
import pandas as pd
import re

data = pd.read_csv('Datasets\\filtered_mobility_data.csv')

provinces = {}

for entry in data.itertuples():
    if entry[4] not in provinces:
        provinces[entry[4]] = [[],[],[],[],[],[]]
        provinces[entry[4]][0].append(entry[6])
        provinces[entry[4]][1].append(entry[7])
        provinces[entry[4]][2].append(entry[8])
        provinces[entry[4]][3].append(entry[9])
        provinces[entry[4]][4].append(entry[10])
        provinces[entry[4]][5].append(entry[11])
    else:
        provinces[entry[4]][0].append(entry[6])
        provinces[entry[4]][1].append(entry[7])
        provinces[entry[4]][2].append(entry[8])
        provinces[entry[4]][3].append(entry[9])
        provinces[entry[4]][4].append(entry[10])
        provinces[entry[4]][5].append(entry[11])


x = [i for i in range(31)]


for province in provinces:
    if province == 'Walloon Brabant':
        x = [i for i in range(24)]
    fig, ax = plt.subplots()
    ax.plot(x, provinces[province][0], label='Recreation', color='blue')
    ax.plot(x, provinces[province][1], label='Grocery', color='yellow')
    ax.plot(x, provinces[province][2], label='Parks', color='red')
    ax.plot(x, provinces[province][3], label='Transit stations', color='green')
    ax.plot(x, provinces[province][4], label='Workplaces', color='purple')
    ax.plot(x, provinces[province][5], label='Residential', color='black')

    ax.set_xlabel('date') 
    ax.set_ylabel('recorded mobility difference')  
    ax.set_title(province)
    ax.legend()  

    plt.show()

