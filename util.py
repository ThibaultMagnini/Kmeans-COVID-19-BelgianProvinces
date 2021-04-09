import pandas as pd
from pretty_html_table import build_table
import matplotlib.pyplot as plt

def look_for_province(list):
    data = pd.read_csv('Datasets\output.csv')
    for entry in data.itertuples():
        if entry[9] == list[0]:
            return entry[1]
    return 


def generate_html_table(dataframe):
    table_html = build_table(dataframe, 'blue_light')
    return table_html


def draw_boxplot(data):
    result = []
    for j in range(len(data[0])):
        temp = []
        for i in range(len(data)):
            temp.append(data[i][j])
        result.append(temp)

    labels = ["Infection rate %", "ICU rate %", "Positive test rate %"]
    plot = plt.boxplot(result, sym='yD', vert=True, patch_artist=True, labels=labels)
    colors = ["red", "green", "yellow", "purple", "cyan", "blue"]
    for patch, color in zip(plot['boxes'], colors):
        patch.set_facecolor(color)
    plt.title("Boxplot representation of the used parameters")
    plt.show()

    return