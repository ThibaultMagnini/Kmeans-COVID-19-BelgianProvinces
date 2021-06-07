import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.dates as mdates

mobility_2020 = pd.read_csv("Datasets\\2020_BE_Region_Mobility_Report.csv", dayfirst=True)
mobility_2021 = pd.read_csv("Datasets\\2021_BE_Region_Mobility_Report.csv", dayfirst=True)
cases = pd.read_csv("Datasets\COVID19BE_CASES_AGESEX.csv")
cases = cases.dropna(subset=["DATE"])

mobility = pd.concat([mobility_2020, mobility_2021])

mobility['sub_region_2'].mask(mobility['sub_region_2'] == 'Antwerp', 'Antwerpen', inplace=True)
mobility['sub_region_2'].mask(mobility['sub_region_2'] == 'East Flanders', 'OostVlaanderen', inplace=True)
mobility['sub_region_2'].mask(mobility['sub_region_2'] == 'Flemish Brabant', 'VlaamsBrabant', inplace=True)
mobility['sub_region_2'].mask(mobility['sub_region_2'] == 'Province of Namur', 'Namur', inplace=True)
mobility['sub_region_2'].mask(mobility['sub_region_2'] == 'Walloon Brabant', 'BrabantWallon', inplace=True)
mobility['sub_region_2'].mask(mobility['sub_region_2'] == 'West Flanders', 'WestVlaanderen', inplace=True)
mobility['sub_region_2'].mask(mobility['sub_region_2'] == 'Liege', 'Liège', inplace=True)

provinces = ["VlaamsBrabant", "WestVlaanderen", "OostVlaanderen", "Namur", "Luxembourg", "Limburg", "Liège", "Hainaut", "Brussels", "BrabantWallon", "Antwerpen"]
sectors = ["retail_and_recreation_percent_change_from_baseline", "grocery_and_pharmacy_percent_change_from_baseline", "parks_percent_change_from_baseline", "transit_stations_percent_change_from_baseline", "workplaces_percent_change_from_baseline", "residential_percent_change_from_baseline"]


with PdfPages('report.pdf') as pdf:
    for province in provinces:
        for sector in sectors:
            data_province = (cases[cases["PROVINCE"] == province])
            data_province = data_province.groupby("DATE", as_index=False).sum()
            data_province = data_province.sort_values("DATE")
            if province == "Brussels":
                data_sector = (mobility[mobility["sub_region_1"] == province])
            else:
                data_sector = (mobility[mobility["sub_region_2"] == province])
            data_sector = data_sector.sort_values("date")
            fig, ax = plt.subplots()
            ax.plot(data_sector["date"], data_sector[sector], label=f"Mobility {sector}")
            ax.plot(data_province["DATE"], data_province["CASES"], label=f"New cases {province}")
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=100))
            plt.xlabel("Dates")
            ax.yaxis.grid()
            plt.title(f"Mobility {sector} for {province}")
            plt.legend()
            pdf.savefig()
            plt.close()
