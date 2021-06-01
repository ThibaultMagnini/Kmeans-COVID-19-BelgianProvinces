import pandas as pd

provinces = ["VlaamsBrabant", "WestVlaanderen", "OostVlaanderen", "Namur", "Luxembourg", "Limburg", "Liège", "Hainaut", "Brussels", "BrabantWallon", "Antwerpen"]
data = pd.read_csv("../../Datasets/COVID19BE_CASES_AGESEX.csv")

for province in provinces:
    data_province = (data[data["PROVINCE"] == province])
    data_province = data_province.dropna(subset=["DATE"])
    data_province = data_province.groupby(["DATE"], as_index=False).sum()
    data_province["DATE"] = pd.to_datetime(data_province["DATE"])
    missingDates = pd.date_range(start="2020-03-01", end="2021-05-25").difference(data_province["DATE"])
    dates_df = pd.DataFrame({"DATE": missingDates, "CASES": 0})
    data_province = pd.concat([data_province, dates_df])
    data_province = data_province.sort_values(by="DATE")
    data_province = data_province.rename(columns={"CASES": "NEW_CASES"})
    data_province["Confirmados"] = data_province["NEW_CASES"].cumsum()
    data_province = data_province.reset_index(drop=True)
    data_province["NEW_RECOVERED"] = 0
    for index, row in data_province.iterrows():
        if index > 13:
            data_province.iloc[index, 3] = data_province.iloc[index - 14, 1]
    data_province["Rt"] = data_province["NEW_RECOVERED"].cumsum()
    data_province["At"] = 0
    for index, row in data_province.iterrows():
        data_province.iloc[index, 5] = data_province.iloc[index, 2] - data_province.iloc[index, 4]
    data_province["Óbitos"] = 0
    data_province = data_province.rename(columns={"DATE": "Data"})
    data_province = data_province[(data_province["Data"] >= "2021-03-01") & (data_province['Data'] <= "2021-05-25")]
    data_province["Data"] = data_province["Data"].dt.strftime("%m/%d/%Y")
    data_province.to_csv(f"../../Datasets/NN/nn_data_{province}.csv", index=False)
