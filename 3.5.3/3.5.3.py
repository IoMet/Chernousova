# import math
# import sqlite3
# from statistics import mean
# import pandas as pd
#
# vacancy_name = input("Введите название профессии: ")
# vacancy_name = f"%{vacancy_name}%"
# con = sqlite3.connect("vdc_db.db")
# cur = con.cursor()
# file_len = cur.execute("SELECT COUNT(*) From vdc_db").fetchall()[0][0]
#
# salaries_year = dict(cur.execute("SELECT years, ROUND(AVG(salary)) From vdc_db "
#                                     "GROUP BY years").fetchall())
#
# vacancies_year = dict(cur.execute("SELECT years, COUNT(name) From vdc_db"
#                                      " GROUP BY years").fetchall())
#
# vacancy_salary = dict(cur.execute("SELECT years, ROUND(AVG(salary)) From vdc_db "
#                                       "WHERE name LIKE :vacancy_name "
#                                       "GROUP BY years", {"vacancy_name": vacancy_name}).fetchall())
#
# vacancy_count = dict(cur.execute("SELECT years, COUNT(name) From vdc_db "
#                                      "WHERE name LIKE :vacancy_name "
#                                      "GROUP BY years", {"vacancy_name": vacancy_name}).fetchall())
#
# salaries_areas = dict(cur.execute("SELECT area_name, ROUND(AVG(salary)) "
#                                   "From vdc_db "
#                                   "GROUP BY area_name "
#                                   "HAVING COUNT(area_name) >= 0.01 * :file_len "
#                                   "ORDER BY ROUND(AVG(salary)) DESC", {"file_len": file_len}).fetchall())
#
# v_a = pd.read_sql("SELECT area_name, COUNT(area_name) From vdc_db "
#                   "GROUP BY area_name "
#                   "ORDER BY COUNT(area_name) DESC "
#                   "LIMIT 10", con)
# v_a["COUNT(area_name)"] = round(v_a['COUNT(area_name)'] / file_len * 100, 2)
# vacancies_areas = dict(v_a[["area_name", 'COUNT(area_name)']].to_dict("split")["data"])
#
# print("Динамика уровня зарплат по годам:", salaries_year)
# print("Динамика количества вакансий по годам:", vacancies_year)
# print("Динамика уровня зарплат по годам для выбранной профессии:", vacancy_salary)
# print("Динамика количества вакансий по годам для выбранной профессии:", vacancy_count)
# print("Уровень зарплат по городам (в порядке убывания):", salaries_areas)
# print("Доля вакансий по городам (в порядке убывания):", vacancies_areas)