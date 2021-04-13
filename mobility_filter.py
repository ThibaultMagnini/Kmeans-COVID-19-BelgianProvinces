from numpy.core.numeric import NaN
import pandas as pd
import numpy as np
import csv
import math
import re

info_mobility_2021 = pd.read_csv('Datasets\\2021_BE_Region_Mobility_Report.csv')
# info_mobility_2020 = pd.read_csv('Datasets\\2020_BE_Region_Mobility_Report.csv')


# info_mobility_2020.drop('metro_area', inplace=True, axis=1)
# info_mobility_2020.drop('iso_3166_2_code', inplace=True, axis=1)
# info_mobility_2020.drop('census_fips_code', inplace=True, axis=1)
# info_mobility_2020.drop('place_id', inplace=True, axis=1)

info_mobility_2021.drop('metro_area', inplace=True, axis=1)
info_mobility_2021.drop('iso_3166_2_code', inplace=True, axis=1)
info_mobility_2021.drop('census_fips_code', inplace=True, axis=1)
info_mobility_2021.drop('place_id', inplace=True, axis=1)

# info_mobility_2020.dropna(inplace=True, axis=0)
info_mobility_2021.dropna(inplace=True, axis=0)

dataframe_march_2021 = info_mobility_2021[info_mobility_2021.date.str.contains('3\/.*\/2021', na = False)]

dataframe_march_2021['sub_region_2'].mask(dataframe_march_2021['sub_region_2'] == 'Antwerp', 'Antwerpen', inplace=True)
dataframe_march_2021['sub_region_2'].mask(dataframe_march_2021['sub_region_2'] == 'East Flanders', 'OostVlaanderen', inplace=True)
dataframe_march_2021['sub_region_2'].mask(dataframe_march_2021['sub_region_2'] == 'Flemish Brabant', 'VlaamsBrabant', inplace=True)
dataframe_march_2021['sub_region_2'].mask(dataframe_march_2021['sub_region_2'] == 'Province of Namur', 'Namur', inplace=True)
dataframe_march_2021['sub_region_2'].mask(dataframe_march_2021['sub_region_2'] == 'Walloon Brabant', 'BrabantWallon', inplace=True)
dataframe_march_2021['sub_region_2'].mask(dataframe_march_2021['sub_region_2'] == 'West Flanders', 'WestVlaanderen', inplace=True)

mean_data = [dataframe_march_2021['sub_region_2'], dataframe_march_2021['retail_and_recreation_percent_change_from_baseline'], dataframe_march_2021['grocery_and_pharmacy_percent_change_from_baseline'], dataframe_march_2021['parks_percent_change_from_baseline'], dataframe_march_2021['transit_stations_percent_change_from_baseline'], dataframe_march_2021['workplaces_percent_change_from_baseline'], dataframe_march_2021['residential_percent_change_from_baseline']]
mean_headers = ['PROVINCE', 'RETAIL_AND_RECREATION', 'GROVERY_AND_PHARMACY', 'PARKS', 'TRANSIT_STATIONS', 'WORKPLACES', 'RESIDENTIAL']
merged_mean_df = pd.concat(mean_data, axis=1, keys=mean_headers)
mean_df = merged_mean_df.groupby('PROVINCE').mean().round(decimals=4)
print(mean_df)
output = pd.read_csv('Datasets\\temp.csv')
output = pd.merge(output, mean_df, on='PROVINCE', how='right')
print(output)
with open('Datasets\\filtered_mobility_data.csv', 'w', newline='') as f:
    dataframe_march_2021.to_csv(f, index=False)

with open('Datasets\\output.csv', 'w', newline='') as f:
    output.to_csv(f, index=False)
# with open('Datasets\\filtered_mobility_data.csv', 'w', newline='') as f:
#     info_mobility_2020.to_csv(f, index=False)
# with open('Datasets\\filtered_mobility_data.csv', 'a', newline='') as f:
#     info_mobility_2021.to_csv(f, index=False)