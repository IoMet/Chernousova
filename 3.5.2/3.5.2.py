# import math
# from statistics import mean
# import pandas as pd
# import sqlite3
#
#
# def set_salary_with_cur(salary_from, salary_to, currency, published_at):
#     published_at = published_at[1] + "/" + published_at[0]
#     currency_value = 0
#
#     if currency != "RUR" and (currency == currency):
#         if currency in ["BYN", "BYR", "EUR", "KZT", "UAH", "USD"]:
#             currency = "BYR" if currency == "BYN" else currency
#             cursor.execute("SELECT * FROM currency_from_api "
#                            "WHERE date == :published_at", {"published_at": published_at})
#             currency_value = cursor.fetchall()[0][currency_dict[currency]]
#     elif currency == "RUR":
#         currency_value = 1
#
#     return check_conditions(salary_from, salary_to, currency_value)
#
#
# def check_conditions(salary_from, salary_to, currency_value):
#     from_nan = math.isnan(salary_from)
#     to_nan = math.isnan(salary_to)
#
#     if from_nan and not to_nan:
#         return salary_to * currency_value
#     elif not from_nan and to_nan:
#         return salary_from * currency_value
#     elif not from_nan and not to_nan:
#         return mean([salary_from, salary_to]) * currency_value
#
#
# df = pd.read_csv("vdc.csv")
# connection = sqlite3.connect("currency_from_api.db")
# cursor = connection.cursor()
# currency_dict = {"BYR": 1, "USD": 2, "EUR": 3, "KZT": 4, "UAH": 5}
#
# df["years"] = df["published_at"].apply(lambda date: date[:4])
# df["salary"] = df.apply(
#     lambda row: set_salary_with_cur(row["salary_from"], row["salary_to"], row["salary_currency"],
#                                     row["published_at"][:7].split("-")), axis=1)
# df = df[df["salary"].notnull()]
#
# new_connection = sqlite3.connect("vdc_db.db")
# new_cursor = new_connection.cursor()
# df.to_sql(name="vdc_db", con=new_connection, if_exists='replace', index=False)
# new_connection.commit()
#
# print("Черноусова Анастасия Сергеевна")
