import pandas as pd
import csv
import math
import re

info_infections = pd.read_csv('Datasets\COVID19BE_CASES_AGESEX.csv')

info_test = pd.read_csv('Datasets\COVID19BE_tests.csv')

info_icu = pd.read_csv('Datasets\COVID19BE_HOSP.csv')

data = {}

def calc_standard(index, result_index):
    # Standardize values for ICU
    # Mean
    mean = 0
    stdev = 0
    for key in data:
        print(key)
        mean += data[key][index]
    mean /= 11    

    # Stdev 
    mean_temp = 0
    for key in data:
        mean_temp += (mean - data[key][index])**2
    mean_temp /= 11 - 1
    stdev = math.sqrt(mean_temp)

    # standardize
    for key in data:
        data[key][result_index] = (data[key][index] - mean) / stdev
    return

# Calculates total confirmed cases per province
for entry in info_infections.itertuples():
    if re.search(r'2021-03-.', str(entry[1])):
        if entry[2] not in data:
            data[entry[2]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            data[entry[2]][0] += entry[6]
            data[entry[2]][7] += entry[6]
        else:
            data[entry[2]][0] += entry[6]
            data[entry[2]][7] += entry[6]

data.pop('nan', None)

# Tests file
for entry in info_test.itertuples():
    if re.search(r'2021-03-.', str(entry[1])):
        if entry[2] not in data:
            data[entry[2]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            data[entry[2]][3] += entry[4]
            data[entry[2]][4] += entry[5]
        else:
            data[entry[2]][3] += entry[4]
            data[entry[2]][4] += entry[5]

# Hospitalisations file
for entry in info_icu.itertuples():
    if re.search(r'2021-03-.', str(entry[1])):
        if entry[2] not in data:
            data[entry[2]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            data[entry[2]][1] += entry[6]
        else:
            data[entry[2]][1] += entry[6]


# Calculates infaction rate by: confirmed cases / province population
data["Antwerpen"][0] /= 1869730
data["Brussels"][0] /= 1218255
data["Liège"][0] /= 1109800
data["Limburg"][0] /= 877370
data["OostVlaanderen"][0] /= 1525255
data["VlaamsBrabant"][0] /= 1155843
data["BrabantWallon"][0] /= 406016
data["WestVlaanderen"][0] /= 1200945
data["Hainaut"][0] /= 1346840
data["Namur"][0] /= 495832
data["Luxembourg"][0] /= 286752

for key in data:
    data[key][0] *= 100
    data[key][0] = round(data[key][0] , 4)


# Filters out NaN value
data = {k:v for k,v in data.items() if v[0] < 20}

# Standardize values for Infection rate
calc_standard(0, 8)


# Calculates ICU rates per province in percentages.
data["Antwerpen"][1] /= data["Antwerpen"][7]
data["Brussels"][1] /= data["Brussels"][7]
data["Liège"][1] /= data["Liège"][7]
data["Limburg"][1] /= data["Limburg"][7]
data["OostVlaanderen"][1] /= data["OostVlaanderen"][7]
data["VlaamsBrabant"][1] /= data["VlaamsBrabant"][7]
data["BrabantWallon"][1] /= data["BrabantWallon"][7]
data["WestVlaanderen"][1] /= data["WestVlaanderen"][7]
data["Hainaut"][1] /= data["Hainaut"][7]
data["Namur"][1] /= data["Namur"][7]
data["Luxembourg"][1] /= data["Luxembourg"][7]

for key in data:
    data[key][1] *= 100
    data[key][1] = round(data[key][1] , 4)

calc_standard(1, 9)


# Test coverage of province (NO CORRECT REPRESENTATION, TESTS CAN BE DONE TWICE ON THE SAME PERSON)
data["Antwerpen"][6] = data["Antwerpen"][3] / 1869730
data["Brussels"][6] = data["Brussels"][3] / 1218255
data["Liège"][6] = data["Liège"][3] / 1109800
data["Limburg"][6] = data["Limburg"][3] / 877370
data["OostVlaanderen"][6] = data["OostVlaanderen"][3] / 1525255
data["VlaamsBrabant"][6] = data["VlaamsBrabant"][3] / 1155843
data["BrabantWallon"][6] = data["BrabantWallon"][3] / 406016
data["WestVlaanderen"][6] = data["WestVlaanderen"][3] / 1200945
data["Hainaut"][6] = data["Hainaut"][3] / 1346840
data["Namur"][6] = data["Namur"][3] / 495832
data["Luxembourg"][6] = data["Luxembourg"][3] / 286752

for key in data:
    data[key][5] = round((data[key][4] / data[key][3]) * 100, 4)

calc_standard(5, 10)

# Formats data for output in CSV
def get_data_for_province(index):
    result = []
    listdict = list(data)
    result.append(listdict[index])
    result.append(data[listdict[index]][0])
    result.append(data[listdict[index]][1])
    result.append(data[listdict[index]][3])
    result.append(data[listdict[index]][4])
    result.append(data[listdict[index]][5])
    # result.append(round(data[listdict[index]][4] / data[listdict[index]][3] * 100, 4))
    result.append(round(data[listdict[index]][6] * 100, 4))
    result.append(data[listdict[index]][7])
    result.append(round(data[listdict[index]][8], 4))
    result.append(round(data[listdict[index]][9], 4))
    result.append(round(data[listdict[index]][10], 4))
    print(result)
    return result

# Writes data to new csv file
headers = ['PROVINCE', 'INFECTION_RATE', 'ICU_RATE', 'TEST_ALL', 'TEST_POS', 'TEST_POS_PERCENTAGE', 'TOTAL_TEST_PERCENTAGE', 'TOTAL_INFECTIONS', 'STANDARD_INFECTION', 'STANDARD_ICU', 'STANDARD_POS_TEST']
with open("Datasets\\output.csv", "w", newline='') as outfile:
   writer = csv.writer(outfile)
   writer.writerow(headers)
   for i in range(len(data)):
      writer.writerow(get_data_for_province(i))

