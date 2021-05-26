import requests
import pandas as pd
import numpy as np
import re
import csv 

############################### DEATHS ########################################

dfMor = pd.read_csv('Datasets\COVID19BE_MORT.csv')
dfMor = dfMor.drop(columns=["REGION","AGEGROUP","SEX"])
dfMor = dfMor.groupby(["DATE"], as_index=False).agg("sum")
dfMor['DEATHSCUM'] = dfMor['DEATHS'].cumsum()

dictmor={}
for entry in dfMor.itertuples():
    if re.search(r'2021-(03|04)-.', str(entry[1])):
        if entry[1] not in dictmor:
            key = re.sub(r'(2021)-(03|04|05)-(.+)', r'\2/\3/\1', entry[1]) 
            dictmor[key] = [0, 0]
            dictmor[key][0] = entry[2]
            dictmor[key][1] = entry[3]

######################## ACTIVE PER DAY ##################################



dfActive = pd.read_csv('Datasets\COVID19BE_CASES_AGESEX.csv')
dfActive = dfActive.drop(columns=["PROVINCE","REGION","AGEGROUP","SEX"])
dfActive = dfActive.groupby(["DATE"], as_index=False).agg("sum")

dictactive = {}
for entry in dfActive.itertuples():
    if re.search(r'2021-(03|04)-.', str(entry[1])):
        if entry[1] not in dictactive:
            dictactive[re.sub(r'(2021)-(03|04|05)-(.+)', r'\2/\3/\1', entry[1]) ] = entry[2] + dfActive["CASES"][entry[0]-14:entry[0]+1].sum()


for key in dictactive.keys():
    dictactive[key] -= dictmor[key][0]


############################## RECOVERED CUMULATIVE #####################################################


r = requests.get(f"https://coronalevel.com/Belgium/datagroup-total-v3.json")

data = r.json()
data = data["series"]
cumulative_confirmed_data = data[0]["data"]
active_data = []

pd.set_option('display.float_format', '{:.2f}'.format)
dfCumConfirmed = pd.DataFrame(cumulative_confirmed_data, columns=['unix', 'CumConfirmedCases'])

dfCumConfirmed = dfCumConfirmed.fillna(0)

dfCumConfirmed = dfCumConfirmed.loc[dfCumConfirmed['unix'] >= 1614553200000.00]
dfCumConfirmed = dfCumConfirmed.loc[dfCumConfirmed['unix'] <= 1619820000000.00]
                                                              
dfCumConfirmed['unix'] = pd.to_datetime(dfCumConfirmed['unix'], unit='ms').dt.date


dictcon={}
for entry in dfCumConfirmed.itertuples():
    if re.search(r'2021-(03|04|05)-.', str(entry[1])):
        if entry[1] not in dictcon:
            dictcon[re.sub(r'(2021)-(03|04|05)-(.+)', r'\2/\3/\1', str(entry[1]))] = int(entry[2])

print(f"Confirmed Cases CUM: \n-------------\n{dictcon}\n-------------------")

dictrec = dictcon.copy()

for key in dictrec.keys():
    dictrec[key] -= dictactive[key]

print(f"Recovered CUM: \n-------------\n{dictrec}\n--------------------")
print(f"Active per Day: \n-------------\n{dictactive}\n")


##############################################################################

with open('Datasets\\nn_data.csv', 'w', newline='') as file:
    csvwriter = csv.writer(file) 
    csvwriter.writerow(["DATE", "ACTIVE", "RECOVERED_CUMULATIVE", "CONFIRMED_CUMULATIVE", "DEATHS"])
    for key in dictactive.keys():
        csvwriter.writerow([key, dictactive[key], dictrec[key], dictcon[key], dictmor[key][1]])

