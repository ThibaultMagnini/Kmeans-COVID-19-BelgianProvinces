import pandas as pd

data = pd.read_csv("..\..\Datasets\COVID19BE_CASES_AGESEX.csv")

inf = pd.read_csv("..\..\Datasets\\belgium_provinces_summed_data.csv")

result = {}

for entry in data.itertuples():
    if entry[1] not in result:
        result[entry[1]] = 0
        result[entry[1]] += entry[6]
    else:
        result[entry[1]] += entry[6]

result_list = list(result.values())

print(inf.to_numpy)