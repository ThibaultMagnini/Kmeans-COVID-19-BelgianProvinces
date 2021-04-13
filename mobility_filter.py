from numpy.core.numeric import NaN
import pandas as pd
import csv
import math
import re

info_mobility_2021 = pd.read_csv('Datasets\\2021_BE_Region_Mobility_Report.csv')
info_mobility_2020 = pd.read_csv('Datasets\\2020_BE_Region_Mobility_Report.csv')


info_mobility_2020.drop('metro_area', inplace=True, axis=1)
info_mobility_2020.drop('iso_3166_2_code', inplace=True, axis=1)
info_mobility_2020.drop('census_fips_code', inplace=True, axis=1)
info_mobility_2020.drop('place_id', inplace=True, axis=1)

info_mobility_2021.drop('metro_area', inplace=True, axis=1)
info_mobility_2021.drop('iso_3166_2_code', inplace=True, axis=1)
info_mobility_2021.drop('census_fips_code', inplace=True, axis=1)
info_mobility_2021.drop('place_id', inplace=True, axis=1)

info_mobility_2020.dropna(inplace=True, axis=0)
info_mobility_2021.dropna(inplace=True, axis=0)

dataframe_march_2021 = info_mobility_2021[info_mobility_2021.date.str.contains('3\/.*\/2021', na = False)]
with open('Datasets\\filtered_mobility_data.csv', 'w', newline='') as f:
    dataframe_march_2021.to_csv(f, index=False)
# with open('Datasets\\filtered_mobility_data.csv', 'w', newline='') as f:
#     info_mobility_2020.to_csv(f, index=False)
# with open('Datasets\\filtered_mobility_data.csv', 'a', newline='') as f:
#     info_mobility_2021.to_csv(f, index=False)