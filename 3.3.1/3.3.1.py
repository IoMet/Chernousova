import pandas as pd
import requests

pd.set_option("expand_frame_repr", False)
file = input("Введите название файла: ")
df = pd.read_csv(file)

df_currency = df["salary_currency"].value_counts()
df_currency = df_currency.apply(lambda currency: currency if currency >= 5000 else False)

start_date = df["published_at"].min()[:7].split("-")
final_date = df["published_at"].max()[:7].split("-")

df_cur_from_api = pd.DataFrame(columns=["date", "BYR", "USD", "EUR", "KZT", "UAH"])


def fill_dataframe(date):
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req=15/{date}d=1"
    response = requests.get(url)
    df_from_xml = pd.read_xml(response.text)
    df_from_xml_f = df_from_xml.loc[df_from_xml['CharCode'].isin(["BYN", "BYR", "EUR", "KZT", "UAH", "USD"])]

    BYR = float(
        df_from_xml_f.loc[df_from_xml_f["CharCode"].isin(["BYR", "BYN"])]["Value"].values[0].replace(',', ".")) / \
          float(df_from_xml_f.loc[df_from_xml_f["CharCode"].isin(["BYR", "BYN"])]["Nominal"].values[0])
    EUR = (get_value(df_from_xml_f, "EUR"))
    KZT = (get_value(df_from_xml_f, "KZT"))
    UAH = (get_value(df_from_xml_f, "UAH"))
    USD = (get_value(df_from_xml_f, "USD"))

    df_cur_from_api.loc[len(df_cur_from_api)] = [date, BYR, EUR, KZT, UAH, USD]


def get_value(data, charcode):
    return float(data.loc[data["CharCode"] == charcode]["Value"].values[0].replace(',', ".")) / \
           float(data.loc[data["CharCode"] == charcode]["Nominal"].values[0])


for year in range(2003, 2023):
    if year == 2022:
        for month in range(1, int(final_date[1]) + 1):
            if 1 <= month <= 9:
                fill_dataframe(f"0{month}/{year}")
            else:
                fill_dataframe(f"{month}/{year}")
    else:
        for month in range(int(start_date[1]), 13):
            if 1 <= month <= 9:
                fill_dataframe(f"0{month}/{year}")
            else:
                fill_dataframe(f"{month}/{year}")

df_cur_from_api.to_csv("currency_from_api.csv", index=False)
