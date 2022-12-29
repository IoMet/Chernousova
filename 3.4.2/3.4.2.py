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
# from concurrent import futures
#
# df_currency_from_api = pd.read_csv("currency_from_api.csv")
#
#
# def multiprocessing(args):
#     vacancy, year = args[0], args[1]
#     process_df = pd.read_csv(f'csv_files\\part_{year}.csv')
#     process_df["salary"] = process_df.apply(
#         lambda row: set_salary_with_cur(row["salary_from"], row["salary_to"], row["salary_currency"],
#                                         row["published_at"][:7].split("-")), axis=1)
#     process_df = process_df[process_df["salary"].notnull()]
#     process_df_df_vac = process_df[process_df["name"].str.contains(vacancy)]
#
#     salaries_year = {year: []}
#     vacancies_year = {year: 0}
#     vacancy_salaries = {year: []}
#     vacancies_count = {year: 0}
#
#     salaries_year[year] = int(process_df['salary'].mean())
#     vacancies_year[year] = len(process_df)
#     vacancy_salaries[year] = int(process_df_df_vac['salary'].mean())
#     vacancies_count[year] = len(process_df_df_vac)
#
#     return_list = [salaries_year, vacancies_year, vacancy_salaries, vacancies_count]
#     return return_list
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
# if __name__ == "__main__":
#     class Report:
#         def __init__(self, vacancy, list_by_year):
#             self.generate_image(vacancy, list_by_year)
#             self.generate_pdf(vacancy, list_by_year)
#
#         @staticmethod
#         def generate_pdf(vacancy, list_by_year):
#             env = Environment(loader=FileSystemLoader('.'))
#             template = env.get_template("3.4.2.html")
#
#             pdf_template = template.render(
#                 {'name': vacancy, 'list_by_year': list_by_year})
#
#             options = {'enable-local-file-access': None}
#             config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
#             pdfkit.from_string(pdf_template, 'report.pdf', configuration=config, options=options)
#
#         @staticmethod
#         def generate_image(vacancy, list_by_year):
#             x_nums = np.arange(len(list_by_year[0].keys()))
#             width = 0.4
#             x_place1 = x_nums - width / 2
#             x_place2 = x_nums + width / 2
#             fig = plt.figure()
#
#             ax = fig.add_subplot(221)
#             ax.set_title("Уровень зарплат по годам")
#             ax.bar(x_place1, list_by_year[0].values(), width, label="средняя з/п")
#             ax.bar(x_place2, list_by_year[1].values(), width, label=f"з/п {vacancy}")
#             ax.legend(fontsize=8)
#             ax.set_xticks(x_nums, list_by_year[0].keys(), rotation="vertical")
#             ax.tick_params(axis="both", labelsize=8)
#             ax.grid(True, axis="y")
#
#             ax = fig.add_subplot(222)
#             ax.set_title("Количество вакансий по годам")
#             ax.bar(x_place1, list_by_year[2].values(), width, label="Количество вакансий")
#             ax.bar(x_place2, list_by_year[3].values(), width, label=f"Количество вакансий \n{vacancy}")
#             ax.tick_params(axis="both", labelsize=8)
#             ax.set_xticks(x_nums, list_by_year[2].keys(), rotation="vertical")
#             ax.legend(fontsize=8)
#             ax.grid(True, axis="y")
#
#             plt.tight_layout()
#             plt.savefig("graph.png")
#
#
#     class MakeChunks:
#         def __init__(self):
#             self.file = input("Введите название файла: ")
#             self.vacancy = input("Введите название профессии: ")
#             self.dataframe = pd.read_csv(self.file)
#
#             self.dataframe["years"] = self.dataframe["published_at"].apply(
#                 lambda date: int(".".join(date[:4].split("-"))))
#             self.years = self.dataframe["years"].unique()
#
#             for year in self.years:
#                 data_to_insert = self.dataframe[self.dataframe["years"] == year]
#                 data_to_insert[["name", "salary_from", "salary_to",
#                                 "salary_currency", "area_name",
#                                 "published_at"]].to_csv(f"csv_files\\part_{year}.csv", index=False)
#
#
#     def sort_dict(dict_to_sort, key):
#         if key == "По ключу":
#             sorted_dict = {}
#             for key in sorted(dict_to_sort):
#                 sorted_dict[key] = dict_to_sort[key]
#             return sorted_dict
#         if key == "По значению":
#             sorted_tuples = sorted(dict_to_sort.items(), key=lambda item: item[1], reverse=True)[:10]
#             sorted_dict = {k: v for k, v in sorted_tuples}
#             return sorted_dict
#
#
#     created_csv = MakeChunks()
#     file_name, vacancy_name = created_csv.file, created_csv.vacancy
#     df = created_csv.dataframe
#     years = created_csv.years
#     salaries_year, vacancies_year, vacancy_salary, vacancy_count = {}, {}, {}, {}
#
#     df["salary"] = df.apply(
#         lambda row: set_salary_with_cur(row["salary_from"], row["salary_to"], row["salary_currency"],
#                                         row["published_at"][:7].split("-")), axis=1)
#     df = df[df["salary"].notnull()]
#
#     with futures.ProcessPoolExecutor() as executor:
#         all_processes = []
#         for year in years:
#             args = (vacancy_name, year)
#             returned_list = executor.submit(multiprocessing, args).result()
#             salaries_year.update(returned_list[0])
#             vacancies_year.update(returned_list[1])
#             vacancy_salary.update(returned_list[2])
#             vacancy_count.update(returned_list[3])
#
#     print("Динамика уровня зарплат по годам:", sort_dict(salaries_year, "По ключу"))
#     print("Динамика количества вакансий по годам:", sort_dict(vacancies_year, "По ключу"))
#     print("Динамика уровня зарплат по годам для выбранной профессии:", sort_dict(vacancy_salary, "По ключу"))
#     print("Динамика количества вакансий по годам для выбранной профессии:", sort_dict(vacancy_count, "По ключу"))
#
#     dicts_by_year = [sort_dict(salaries_year, "По ключу"), sort_dict(vacancy_salary, "По ключу"),
#                      sort_dict(vacancies_year, "По ключу"), sort_dict(vacancy_count, "По ключу")]
#     report = Report(vacancy_name, dicts_by_year)