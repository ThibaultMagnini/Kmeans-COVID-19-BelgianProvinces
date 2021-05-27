import requests
import pandas as pd
import numpy as np
import re
import csv 

############################### DEATHS ########################################

dfMor = pd.read_csv('..\Datasets\COVID19BE_MORT.csv')
dfMor = dfMor.drop(columns=["REGION","AGEGROUP","SEX"])

dfMor = dfMor.groupby(["DATE"], as_index=False).agg("sum")

dfMor['DATE'] = pd.to_datetime(dfMor.DATE)

missingDates = pd.date_range(start='2020-03-01', end='2021-05-25').difference(dfMor.DATE)

dfMor['DATE'] = dfMor['DATE'].dt.strftime('%m/%d/%Y')
dfMor['DEATHSCUM'] = dfMor['DEATHS'].cumsum()

data = []
for i in range(1,10):
    data.insert(i-1, {"DATE":f"03/0{i}/2020", "DEATHS":0, "DEATHSCUM": 0})
dfMor = pd.concat([pd.DataFrame(data), dfMor], ignore_index=True)

print(dfMor.head())

dictmor={}
for entry in dfMor.itertuples():
    # if re.search(r'2021-(03|04)-.', str(entry[1])):
    if entry[1] not in dictmor:
        key = entry[1]
        dictmor[key] = [0, 0]
        dictmor[key][0] = entry[2]
        dictmor[key][1] = entry[3]

######################## ACTIVE PER DAY #################################


############################## RECOVERED CUMULATIVE #####################################################


dataCon = pd.read_csv('..\Datasets\COVID19BE_CASES_AGESEX.csv')
dataCon = dataCon.drop(columns=["PROVINCE","REGION","AGEGROUP","SEX"])
dataCon = dataCon.groupby(["DATE"], as_index=False).agg("sum")
dataCon['DATE'] = pd.to_datetime(dataCon.DATE)
dataCon['DATE'] = dataCon['DATE'].dt.strftime('%m/%d/%Y')
dataCon['CASES'] = dataCon['CASES'].cumsum()

print(dataCon)

dictcon={}
for entry in dataCon.itertuples():
    if entry[1] not in dictcon:
        dictcon[str(entry[1])] = int(entry[2])

dictrec = dictcon.copy()

keyslist=list(dictcon.keys())

for i in range(len(keyslist)):
    if i > 14:
        dictrec[keyslist[i]] = dictcon[keyslist[i-14]] - dictmor[keyslist[i-14]][1]
    else:
        dictrec[keyslist[i]] = 0

print(dictrec)


######################################################################################

dfActive = pd.read_csv('..\Datasets\COVID19BE_CASES_AGESEX.csv')
dfActive = dfActive.drop(columns=["PROVINCE","REGION","AGEGROUP","SEX"])
dfActive = dfActive.groupby(["DATE"], as_index=False).agg("sum")
dfActive['DATE'] = pd.to_datetime(dfActive.DATE)
dfActive['DATE'] = dfActive['DATE'].dt.strftime('%m/%d/%Y')

dictactive = {}
for entry in dfActive.itertuples():
    if entry[1] not in dictactive:
        dictactive[entry[1]] = 0

for key in dictactive.keys():
    dictactive[key] = dictcon[key] - dictrec[key] - dictmor[key][1]

######################################################################################

with open('..\Datasets\\nn_data.csv', 'w', newline='', encoding='UTF-8') as file:
    csvwriter = csv.writer(file) 
    csvwriter.writerow(["Data", "At", "Rt", "Confirmados", "Óbitos"])
    for key in dictactive.keys():
        if(re.search(r'(03|04|05)/.+/2021', key)):
            csvwriter.writerow([key, dictactive[key], dictrec[key], dictcon[key], dictmor[key][1]])

