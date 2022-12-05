import cProfile
import csv
from datetime import datetime
import os
import re

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


def make_exit(msg):
    print(msg)
    exit(0)


class UserInput:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy_name = input('Введите название профессии: ')


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
    published_at = []

    def __init__(self, all_vac):
        for one_vac in all_vac:
            for key, value in one_vac.items():
                if key == 'published_at':
                    self.published_at.append(self.profile_year(value))

    @staticmethod
    def profile_year(data):
        # new_data = int(datetime.strptime(data, '%Y-%m-%dT%H:%M:%S%z').strftime("%Y"))
        # new_data = int(".".join(data[:4].split("-")))
        parts = data[:19].split('T')
        date = parts[0].split('-')
        new_data = int(date[0])
        return new_data


def prepare(text):
    text = re.sub('<.*?>', '', text)
    text = text.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in text.split('\n')]
    return res[0] if len(res) == 1 else res


inputed = UserInput()
dataset = DataSet(inputed.file_name)

titles = dataset.titles
parsed_vac = dataset.parsed_vacancies

all_vacancies = []

for one_parsed_vac in parsed_vac:
    all_vacancies.append(dict(zip(titles, map(prepare, one_parsed_vac))))

cProfile.run('Vacancy(all_vacancies)')