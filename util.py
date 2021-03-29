import pandas as pd
from pretty_html_table import build_table

def look_for_province(list):
    data = pd.read_csv('covid_belgium\Datasets\output.csv')
    for entry in data.itertuples():
        if entry[9] == list[0]:
            return entry[1]
    return 


def generate_html_table(dataframe):
    table_html = build_table(dataframe, 'blue_light')
    return table_html
