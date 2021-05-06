import requests
import pandas as pd
import numpy as np

provinces = ["Antwerp", "Brussels", "East_Flanders", "Flemish_Brabant", "Hainaut", "Liege", "Limburg", "Luxembourg", "Namur", "Walloon_Brabant", "West_Flanders"]

data_confirmed = {"provinces": []}
data_recovered = {"provinces": []}
data_total = {"provinces": []}

for province in provinces:
    data_confirmed["provinces"].append(province)
    data_recovered["provinces"].append(province)
    data_total["provinces"].append(province)
    r = requests.get(f"https://coronalevel.com/Belgium/{province}/datagroup-total-v3.json")
    data = r.json()
    data = data["series"]
    confirmed_data = data[0]["data"]
    recovered_data = data[2]["data"]

    for number in confirmed_data:
        if number[0] not in data_total:
            data_total[number[0]] = []
        data_total[number[0]].append(number[1])

    for i in range(len(confirmed_data)):
        confirmed_data[i][1] = confirmed_data[i][1] - recovered_data[i][1]

    for number in confirmed_data:
        if number[0] not in data_confirmed:
            data_confirmed[number[0]] = []
        data_confirmed[number[0]].append(number[1])

    for number in recovered_data:
        if number[0] not in data_recovered:
            data_recovered[number[0]] = []
        data_recovered[number[0]].append(number[1])

pd_confirmed = pd.DataFrame(data=data_confirmed, dtype=np.double)
pd_recovered = pd.DataFrame(data=data_recovered, dtype=np.double)
pd_total = pd.DataFrame(data=data_total, dtype=np.double)

with open('Datasets\\belgium_provinces_total_cases.csv', 'w+', newline='') as f:
    pd_total.to_csv(f, index=False)

with open('Datasets\\belgium_provinces_active_cases.csv', 'w+', newline='') as f:
    pd_confirmed.to_csv(f, index=False)

with open('Datasets\\belgium_provinces_recovered_cases.csv', 'w+', newline='') as f:
    pd_recovered.to_csv(f, index=False)