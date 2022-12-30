# import math
# from statistics import mean
# import openpyxl
# from openpyxl.styles import Font, Border, Side
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib import ticker
# import pdfkit
# from jinja2 import Environment, FileSystemLoader
# import pandas as pd
#
#
# class Report:
#     def __init__(self, vacancy, reg, list_by_area, list_by_year, others_info):
#         self.generate_image(vacancy, reg, list_by_area, list_by_year, others_info)
#         self.generate_pdf(vacancy, reg, list_by_area, list_by_year)
#
#     @staticmethod
#     def generate_pdf(vacancy, reg, list_by_area, list_by_year):
#         env = Environment(loader=FileSystemLoader('.'))
#         template = env.get_template("3.4.3.html")
#
#         pdf_template = template.render(
#             {'name': vacancy_name, "region": reg, 'list_by_year': list_by_year, 'list_by_area': list_by_area,
#              'area_td_1': list(list_by_area[0].keys()), 'area_td_2': list(list_by_area[0].values()),
#              'area_td_3': list(list_by_area[1].keys()), 'area_td_4': list(list_by_area[1].values())})
#
#         options = {'enable-local-file-access': None}
#         config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
#         pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options=options)
#
#     @staticmethod
#     def generate_image(vacancy, reg, list_by_area, list_by_year, others_info):
#         x_nums = np.arange(len(list_by_year[0].keys()))
#         width = 0.4
#         fig = plt.figure()
#
#         ax = fig.add_subplot(221)
#         ax.set_title("Уровень зарплат по годам")
#         ax.bar(x_nums, list_by_year[0].values(), width, label=f"з/п {vacancy.lower()}, {reg}")
#         ax.legend(fontsize=8)
#         ax.set_xticks(x_nums, list_by_year[0].keys(), rotation="vertical")
#         ax.tick_params(axis="both", labelsize=8)
#         ax.grid(True, axis="y")
#
#         ax = fig.add_subplot(222)
#         ax.set_title("Количество вакансий по годам")
#         ax.bar(x_nums, list_by_year[1].values(), width, label=f"Количество вакансий \n{vacancy.lower()}, {reg}")
#         ax.tick_params(axis="both", labelsize=8)
#         ax.set_xticks(x_nums, list_by_year[1].keys(), rotation="vertical")
#         ax.legend(fontsize=8)
#         ax.grid(True, axis="y")
#
#         width = 0.8
#         y_ticks_cities = np.arange(len(list_by_area[0].keys()))
#         y_ticks_cities_names = {}
#         for key, value in list_by_area[0].items():
#             if "-" in key or " " in key:
#                 key = key.replace("-", "-\n")
#                 key = key.replace(" ", "\n")
#             y_ticks_cities_names[key] = value
#
#         ax = fig.add_subplot(223)
#         ax.set_title("Уровень зарплат по городам")
#         ax.barh(y_ticks_cities, list_by_area[0].values(), width, align="center")
#         ax.xaxis.set_major_locator(ticker.MultipleLocator(100000))
#         ax.set_yticks(y_ticks_cities, labels=y_ticks_cities_names.keys(), horizontalalignment="right",
#                       verticalalignment="center")
#         ax.tick_params(axis="x", labelsize=8)
#         ax.tick_params(axis="y", labelsize=6)
#         ax.invert_yaxis()
#         ax.grid(True, axis="x")
#
#         ax = fig.add_subplot(224)
#         ax.set_title("Доля вакансий по городам")
#         list_by_area[1]["Другие"] = others
#         ax.pie(list_by_area[1].values(), labels=list_by_area[1].keys(), textprops={'size': 6},
#                colors=["#ff8006", "#28a128", "#1978b5", "#0fbfd0",
#                        "#bdbe1c", "#808080", "#e478c3", "#8d554a",
#                        "#9567be", "#d72223", "#1978b5", "#ff8006"])
#         ax.axis('equal')
#
#         plt.tight_layout()
#         plt.savefig("graph.png")
#
#
# def set_salary_with_cur(salary_from, salary_to, currency, published_at):
#     published_at = published_at[1] + "/" + published_at[0]
#     currency_value = 0
#
#     if currency != "RUR" and (currency == currency):
#         if currency in ["BYN", "BYR", "EUR", "KZT", "UAH", "USD"]:
#             currency = "BYR" if currency == "BYN" else currency
#             df_currency_from_api_row = df_currency_from_api.loc[df_currency_from_api["date"] == published_at]
#             currency_value = df_currency_from_api_row[currency].values[0]
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
# def sort_dict(dict_to_sort, key):
#     if key == "По ключу":
#         sorted_dict = {}
#         for key in sorted(dict_to_sort):
#             sorted_dict[key] = dict_to_sort[key]
#         return sorted_dict
#     if key == "По значению":
#         sorted_tuples = sorted(dict_to_sort.items(), key=lambda item: item[1], reverse=True)[:10]
#         sorted_dict = {k: v for k, v in sorted_tuples}
#         return sorted_dict
#
#
# file_name = input("Введите название файла: ")
# vacancy_name = input("Введите название профессии: ")
# region = input("Введите название региона: ")
# df = pd.read_csv(file_name)
# df_currency_from_api = pd.read_csv("currency_from_api.csv")
# vacancy_salary, vacancy_count, salaries_areas, vacancies_areas = {}, {}, {}, {}
#
# df["years"] = df["published_at"].apply(lambda date: int(".".join(date[:4].split("-"))))
# years = df["years"].unique()
#
# df["salary"] = df.apply(
#     lambda row: set_salary_with_cur(row["salary_from"], row["salary_to"], row["salary_currency"],
#                                     row["published_at"][:7].split("-")), axis=1)
# df = df[df["salary"].notnull()]
#
# df_vacancy = df[df["name"].str.contains(vacancy_name)]
# for year in years:
#     df_vacancy_sorted = df_vacancy[(df_vacancy['years'] == year) & (df_vacancy['area_name'] == region)]
#     if not df_vacancy_sorted.empty:
#         vacancy_salary[year] = int(df_vacancy_sorted['salary'].mean())
#         vacancy_count[year] = len(df_vacancy_sorted)
#
# vacancies = len(df)
# df["count"] = df.groupby("area_name")['area_name'].transform("count")
# df_norm = df[df['count'] >= 0.01 * vacancies]
# cities = list(df_norm["area_name"].unique())
# others = len(df[df['count'] < 0.01 * vacancies]) / vacancies
#
# for city in cities:
#     df_s = df_norm[df_norm['area_name'] == city]
#     salaries_areas[city] = int(df_s['salary'].mean())
#     vacancies_areas[city] = round(len(df_s) / len(df), 4)
#
# print("Уровень зарплат по городам (в порядке убывания):", sort_dict(salaries_areas, "По значению"))
# print("Доля вакансий по городам (в порядке убывания):", sort_dict(vacancies_areas, "По значению"))
# print("Динамика уровня зарплат по годам для выбранной профессии и региона:", sort_dict(vacancy_salary, "По ключу"))
# print("Динамика количества вакансий по годам для выбранной профессии и региона:", sort_dict(vacancy_count, "По ключу"))
#
# dicts_by_area = [sort_dict(salaries_areas, "По значению"), sort_dict(vacancies_areas, "По значению")]
# dicts_by_year = [sort_dict(vacancy_salary, "По ключу"), sort_dict(vacancy_count, "По ключу")]
#
# report = Report(vacancy_name, region, dicts_by_area, dicts_by_year, others)
