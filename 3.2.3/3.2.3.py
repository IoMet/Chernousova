import pandas as pd
from concurrent import futures


def multiprocessing(args):
    vacancy, year = args[0], args[1]
    process_df = pd.read_csv(f'csv_files\\part_{year}.csv')
    process_df['salary'] = process_df[['salary_from', 'salary_to']].mean(axis=1)
    process_df_df_vac = process_df[process_df["name"].str.contains(vacancy)]

    salaries_year = {year: []}
    vacancies_year = {year: 0}
    vacancy_salaries = {year: []}
    vacancies_count = {year: 0}

    salaries_year[year] = int(process_df['salary'].mean())
    vacancies_year[year] = len(process_df)
    vacancy_salaries[year] = int(process_df_df_vac['salary'].mean())
    vacancies_count[year] = len(process_df_df_vac)

    return_list = [salaries_year, vacancies_year, vacancy_salaries, vacancies_count]
    return return_list


if __name__ == "__main__":
    class MakeChunks:
        def __init__(self):
            self.file = input("Введите название файла: ")
            self.vacancy = input("Введите название профессии: ")
            self.dataframe = pd.read_csv(self.file)

            self.dataframe["years"] = self.dataframe["published_at"].apply(
                lambda date: int(".".join(date[:4].split("-"))))
            self.years = self.dataframe["years"].unique()

            for year in self.years:
                data_to_insert = self.dataframe[self.dataframe["years"] == year]
                data_to_insert[["name", "salary_from", "salary_to",
                                "salary_currency", "area_name",
                                "published_at"]].to_csv(f"csv_files\\part_{year}.csv", index=False)


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


    created_csv = MakeChunks()
    file_name, vacancy_name = created_csv.file, created_csv.vacancy
    df = created_csv.dataframe
    years = created_csv.years
    salaries_year, vacancies_year, vacancy_salary, vacancy_count, salaries_areas, vacancies_areas \
        = {}, {}, {}, {}, {}, {}

    df["published_at"] = df["published_at"].apply(lambda date: int(".".join(date[:4].split("-"))))
    df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)

    with futures.ProcessPoolExecutor() as executor:
        all_processes = []
        for year in years:
            args = (vacancy_name, year)
            returned_list = executor.submit(multiprocessing, args).result()
            salaries_year.update(returned_list[0])
            vacancies_year.update(returned_list[1])
            vacancy_salary.update(returned_list[2])
            vacancy_count.update(returned_list[3])

    df["count"] = df.groupby("area_name")['area_name'].transform("count")
    df_norm = df[df['count'] >= 0.01 * len(df)]
    cities = list(df_norm["area_name"].unique())

    for city in cities:
        df_by_city = df_norm[df_norm['area_name'] == city]
        salaries_areas[city] = int(df_by_city['salary'].mean())
        vacancies_areas[city] = round(len(df_by_city) / len(df), 4)

    print("Динамика уровня зарплат по годам:", sort_dict(salaries_year, "По ключу"))
    print("Динамика количества вакансий по годам:", sort_dict(vacancies_year, "По ключу"))
    print("Динамика уровня зарплат по годам для выбранной профессии:", sort_dict(vacancy_salary, "По ключу"))
    print("Динамика количества вакансий по годам для выбранной профессии:", sort_dict(vacancy_count, "По ключу"))
    print("Уровень зарплат по городам (в порядке убывания):", sort_dict(salaries_areas, "По значению"))
    print("Доля вакансий по городам (в порядке убывания):", sort_dict(vacancies_areas, "По значению"))
