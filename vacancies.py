import os
import re
import csv
from prettytable import PrettyTable
from datetime import datetime

dic_experience = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет",
}

dic_experience_reversed = {
    "Нет опыта": 0,
    "От 1 года до 3 лет": 1,
    "От 3 до 6 лет": 2,
    "Более 6 лет": 3,
}

dic_currency = {
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
}

dic_sal_gross = {
    'True': 'Без вычета налогов',
    'False': 'С вычетом налогов',
    'TRUE': 'Без вычета налогов',
    'FALSE': 'С вычетом налогов',
}

dic_premium = {
    'True': 'Да',
    'False': 'Нет',
    'TRUE': 'Да',
    'FALSE': 'Нет',
}

currency_to_rub = {
    "Манаты": 35.68,
    "Белорусские рубли": 23.91,
    "Евро": 59.90,
    "Грузинский лари": 21.74,
    "Киргизский сом": 0.76,
    "Тенге": 0.13,
    "Рубли": 1,
    "Гривны": 1.64,
    "Доллары": 60.66,
    "Узбекский сум": 0.0055,
}

translate_to_eng = {
    "Название": 'name',
    "Описание": 'description',
    "Навыки": 'key_skills',
    "Опыт работы": 'experience_id',
    "Премиум-вакансия": 'premium',
    "Компания": 'employer_name',
    "Нижняя граница вилки оклада": 'salary_from',
    "Верхняя граница вилки оклада": 'salary_to',
    "Оклад указан до вычета налогов": 'salary_gross',
    "Идентификатор валюты оклада": 'salary_currency',
    "Оклад": 'salary',
    "Название региона": 'area_name',
    "Дата публикации вакансии": 'published_at',
}

filter_columns = ["Название", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                  "Идентификатор валюты оклада", "Название региона", "Дата публикации вакансии"]

sort_columns = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия",
                "Компания", "Оклад", "Название региона", "Дата публикации вакансии"]


def make_exit(text):
    print(text)
    exit(0)


class UserInput:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.filter_input = input('Введите параметр фильтрации: ')
        self.sort_input = input('Введите параметр сортировки: ')
        self.r_sort_input = input('Обратный порядок сортировки (Да / Нет): ')
        self.numbers_input = input('Введите диапазон вывода: ').split()
        self.titles_input = self.accept_titles(input('Введите требуемые столбцы: ').split(', '))

        self.filter_input = self.accept_filter_input(self.filter_input)
        self.sort_input = self.accept_sort_input(self.sort_input)
        self.r_sort_input = self.accept_r_sort_input(self.r_sort_input)

    @staticmethod
    def accept_filter_input(filter_input):
        if filter_input != "" and ": " not in filter_input:
            make_exit("Формат ввода некорректен")

        if filter_input != "" and filter_input.split(": ")[0] not in filter_columns:
            make_exit("Параметр поиска некорректен")
        return filter_input

    @staticmethod
    def accept_sort_input(sort_input):
        if sort_input != "" and sort_input not in sort_columns:
            make_exit("Параметр сортировки некорректен")
        return sort_input

    @staticmethod
    def accept_r_sort_input(r_sort_input):
        if r_sort_input not in ["Да", "Нет", ""]:
            make_exit("Порядок сортировки задан некорректно")
        return r_sort_input == "Да"

    @staticmethod
    def accept_titles(lst_names):
        if "" in lst_names:
            lst_names = ["Название", "Описание", "Навыки",
                         "Опыт работы", "Премиум-вакансия", 'Компания',
                         'Оклад', 'Название региона', 'Дата публикации вакансии']
        lst_names.insert(0, "№")
        return lst_names


class DataSet:
    def __init__(self, file_name):
        if os.stat(file_name).st_size == 0:
            make_exit("Пустой файл")

        self.vacancies = [row for row in csv.reader(open(file_name, encoding="utf_8_sig"))]
        self.titles = self.vacancies[0]
        self.parsed_vacancies = [row for row in self.vacancies[1:] if
                                 len(row) == len(self.titles) and row.count('') == 0]

        if len(self.parsed_vacancies) == 0:
            make_exit('Нет данных')


class Vacancy:
    def __init__(self, one_vac):
        for key, value in one_vac.items():
            if key == 'key_skills' and type(value) == list:
                self.key_skills = "\n".join(value)
            elif key == 'key_skills' and type(value) == str:
                self.key_skills = value
            elif key == 'premium':
                self.premium = dic_premium[value]
            elif key == 'salary_gross':
                self.salary_gross = dic_sal_gross[value]
            elif key == 'experience_id':
                self.experience_id = dic_experience[value]
            elif key == 'salary_currency':
                self.salary_currency = dic_currency[value]
            elif key == "salary_to":
                self.salary_to = '{:,}'.format(int(float(value))).replace(',', ' ')
            elif key == "salary_from":
                self.salary_from = '{:,}'.format(int(float(value))).replace(',', ' ')
            elif key == 'published_at':
                self.full_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S%z').strftime("%d.%m.%Y-%H:%M:%S")
                self.published_at = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S%z').strftime("%d.%m.%Y")
            elif key == "name":
                self.name = value
            elif key == "description":
                self.description = value
            elif key == "employer_name":
                self.employer_name = value
            elif key == "area_name":
                self.area_name = value

        self.salary = f'{self.salary_from} - {self.salary_to} ({self.salary_currency}) ({self.salary_gross})'

    def make_filter(self, filter_input):
        if filter_input == '':
            return True

        filter_input = filter_input.split(': ')
        if filter_input[0] == 'Оклад':
            return float(self.salary_from.replace(' ', '')) <= float(filter_input[1]) <= float(
                self.salary_to.replace(' ', ''))
        elif filter_input[0] == 'Идентификатор валюты оклада':
            return self.salary_currency == filter_input[1]
        elif filter_input[0] == 'Навыки':
            for skill in filter_input[1].split(", "):
                if skill not in self.key_skills.split("\n"):
                    return False
            return True
        else:
            return self.__dict__[translate_to_eng[filter_input[0]]] == filter_input[1]


class Table:
    def __init__(self):
        self.table = PrettyTable(["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия",
                                  'Компания', 'Оклад', 'Название региона', 'Дата публикации вакансии'])
        self.table.hrules = 1
        self.table.align = "l"
        self.table.max_width = 20

    @staticmethod
    def accept_numbers(result_vac, list_numbers):
        if len(result_vac) == 0:
            make_exit('Ничего не найдено')

        if len(list_numbers) >= 1:
            start = int(list_numbers[0]) - 1
        else:
            start = 0

        if len(list_numbers) >= 2:
            end = int(list_numbers[1]) - 1
        else:
            end = len(result_vac)

        return start, end

    def print(self, result_vac, list_numbers, list_titles):
        (start, end) = self.accept_numbers(result_vac, list_numbers)

        for i, one_vac in enumerate(result_vac):
            row = [i + 1]
            for title in self.table.field_names[1:]:
                one_vac_value = one_vac.__dict__[translate_to_eng[title]]

                if len(one_vac_value) > 100:
                    one_vac_value = one_vac_value[:100] + "..."
                row.append(one_vac_value)
            self.table.add_row(row)

        print(self.table.get_string(start=start, end=end, fields=list_titles))


class PrepareVacData:
    def prepare_vacancies(self, all_vacancies, filter_input, sort_input, r_sort_input, titles):
        filtered_vac = []
        for one_vac in all_vacancies:
            parsed_vacancies = Vacancy(dict(zip(titles, map(self.prepare_vac, one_vac))))
            if parsed_vacancies.make_filter(filter_input):
                filtered_vac.append(parsed_vacancies)
        return self.make_sort(filtered_vac, sort_input, r_sort_input)

    @staticmethod
    def prepare_vac(text):
        text = re.sub('<.*?>', '', text)
        text = text.replace("\r\n", "\n")
        res = [' '.join(word.split()) for word in text.split('\n')]
        return res[0] if len(res) == 1 else res

    def make_sort(self, filtered_vac, sort_input, r_sort_input):
        if sort_input == "":
            return filtered_vac

        return sorted(filtered_vac, key=lambda one_vac: self.get_sort(one_vac, sort_input), reverse=r_sort_input)

    @staticmethod
    def get_sort(one_vac, sort_input):
        if sort_input == "Навыки":
            return len(one_vac.key_skills.split("\n"))
        elif sort_input == "Оклад":
            return currency_to_rub[one_vac.salary_currency] * (
                    float(one_vac.salary_from.replace(' ', '')) + float(one_vac.salary_to.replace(' ', ''))) // 2
        elif sort_input == "Дата публикации вакансии":
            return one_vac.full_time
        elif sort_input == "Опыт работы":
            return dic_experience_reversed[one_vac.experience_id]
        else:
            return one_vac.__getattribute__(translate_to_eng[sort_input])


class Initialization:
    def __init__(self):
        inputed = UserInput()
        dataset = DataSet(inputed.file_name)

        titles = dataset.titles
        parsed_vac = dataset.parsed_vacancies

        prepare_vac = PrepareVacData()

        result_vacancies = prepare_vac.prepare_vacancies(parsed_vac, inputed.filter_input, inputed.sort_input,
                                                         inputed.r_sort_input, titles)

        table = Table()
        table.print(result_vacancies, inputed.numbers_input, inputed.titles_input)
