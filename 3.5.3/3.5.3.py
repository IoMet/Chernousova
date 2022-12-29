import math
import sqlite3
from statistics import mean
import pandas as pd


def sort_dict(dict_to_sort, key):
    if key == "По ключу":
        sorted_dict = {}
        for key in sorted(dict_to_sort):
            sorted_dict[key] = dict_to_sort[key]
        return sorted_dict
    if key == "По значению":
        sorted_tuples = sorted(dict_to_sort.items(), key=lambda item: item[1], reverse=True)[:10]
        sorted_dict = {k: v for k, v in sorted_tuples}
        return sorted_dict


vacancy_name = input("Введите название профессии: ")
vacancy_name = f"%{vacancy_name}%"
con = sqlite3.connect("new_vac_with_dif_currencies.db")
cur = con.cursor()
database_length = pd.read_sql("SELECT COUNT(*) From new_vac_with_dif_currencies", con).to_dict()["COUNT(*)"][0]

s_groups_by_y = pd.read_sql("SELECT years, ROUND(AVG(salary)) From new_vac_with_dif_currencies GROUP BY years", con)
salaries_by_year = dict(s_groups_by_y[["years", "ROUND(AVG(salary))"]].to_dict("split")["data"])

v_groups_by_y = pd.read_sql("SELECT years, COUNT(name) From new_vac_with_dif_currencies GROUP BY years", con)
vacancies_by_year = dict(v_groups_by_y[["years", "COUNT(name)"]].to_dict("split")["data"])

i_v_s_groups_by_y = pd.read_sql("SELECT years, ROUND(AVG(salary)) From new_vac_with_dif_currencies "
                                "WHERE name LIKE :vacancy_name "
                                "GROUP BY years", con, params=[vacancy_name])
inp_vacancy_salary = dict(i_v_s_groups_by_y[["years", "ROUND(AVG(salary))"]].to_dict("split")["data"])

i_v_c_groups_by_y = pd.read_sql("SELECT years, COUNT(name) From new_vac_with_dif_currencies "
                                "WHERE name LIKE :vacancy_name "
                                "GROUP BY years", con, params=[vacancy_name])
inp_vacancy_count = dict(i_v_c_groups_by_y[["years", "COUNT(name)"]].to_dict("split")["data"])

s_a_groups_by_c = pd.read_sql("SELECT area_name, ROUND(AVG(salary)), COUNT(area_name) From new_vac_with_dif_currencies "
                              "GROUP BY area_name "
                              "ORDER BY COUNT(area_name) DESC ", con)

s_a_groups_by_c = s_a_groups_by_c[s_a_groups_by_c["COUNT(area_name)"] >= 0.01 * database_length]
salaries_areas = dict(s_a_groups_by_c[["area_name", "ROUND(AVG(salary))"]].to_dict("split")["data"])
salaries_areas = sort_area_dict(salaries_areas)

v_a_groups_by_c = pd.read_sql("SELECT area_name, COUNT(area_name) From new_vac_with_dif_currencies "
                              "GROUP BY area_name "
                              "ORDER BY COUNT(area_name) DESC "
                              "LIMIT 10", con)
v_a_groups_by_c["COUNT(area_name)"] = round(v_a_groups_by_c["COUNT(area_name)"] / database_length * 100, 2)
vacancies_areas = dict(v_a_groups_by_c[["area_name", 'COUNT(area_name)']].to_dict("split")["data"])

print("Динамика уровня зарплат по годам:", salaries_year)
print("Динамика количества вакансий по годам:", vacancies_year)
print("Динамика уровня зарплат по годам для выбранной профессии:", vacancy_salary)
print("Динамика количества вакансий по годам для выбранной профессии:", vacancy_count)
print("Уровень зарплат по городам (в порядке убывания):", sort_dict(salaries_areas, "По значению"))
print("Доля вакансий по городам (в порядке убывания):", sort_dict(vacancies_areas, "По значению"))