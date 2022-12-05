import re
from unittest import TestCase
import tests

file_name = "vacancies.csv"
vac_name = "Программист"
dataset = tests.DataSet(file_name)
titles = dataset.titles


class VacancyTest(TestCase):
    parsed_vac_1 = dataset.parsed_vacancies[0]
    parsed_vac_2 = {"name": "Программист", "salary_from": "100.0", "salary_to": "5000.0", "salary_currency": "USD",
                    "area_name": "тута", "published_at": "2022-01-12T14:12:06-0500"}

    @staticmethod
    def prepare(text):
        text = re.sub('<.*?>', '', text)
        text = text.replace("\r\n", "\n")
        res = [' '.join(word.split()) for word in text.split('\n')]
        return res[0] if len(res) == 1 else res

    def test_salary(self):
        vac = tests.Vacancy(dict(zip(titles, map(self.prepare, self.parsed_vac_1))))
        self.assertEqual(vac.salary, 90000)

    def test_salary_type(self):
        vac = tests.Vacancy(dict(zip(titles, map(self.prepare, self.parsed_vac_1))))
        self.assertEqual(type(vac.salary).__name__, "int")

    def test_salary_from(self):
        vac = tests.Vacancy(dict(zip(titles, map(self.prepare, self.parsed_vac_1))))
        self.assertEqual(vac.salary_from, "80 000")

    def test_salary_to(self):
        vac = tests.Vacancy(dict(zip(titles, map(self.prepare, self.parsed_vac_1))))
        self.assertEqual(vac.salary_to, "100 000")

    def test_salary_currency(self):
        vac = tests.Vacancy(dict(zip(titles, map(self.prepare, self.parsed_vac_1))))
        self.assertEqual(vac.salary_currency, "Рубли")

    def test_salary_area_name(self):
        vac = tests.Vacancy(dict(zip(titles, map(self.prepare, self.parsed_vac_1))))
        self.assertEqual(vac.area_name, "Санкт-Петербург")

    def test_salary_published(self):
        vac = tests.Vacancy(dict(zip(titles, map(self.prepare, self.parsed_vac_1))))
        self.assertEqual(vac.published_at, 2022)

    def test_salary_name(self):
        vac = tests.Vacancy(dict(zip(titles, map(self.prepare, self.parsed_vac_1))))
        self.assertEqual(vac.name, "Руководитель проекта по системам связи и информационным технологиям")

    def test_salary_from_type(self):
        vac = tests.Vacancy(self.parsed_vac_2)
        self.assertEqual(type(vac.salary_from).__name__, "str")


class ResultStaticTest(TestCase):
    result = tests.ResultStatic()
    correct_dict = {"Доллары": 60.66, "Евро": 59.90, "Манаты": 35.68, "Белорусские рубли": 23.91,
                    "Грузинский лари": 21.74, "Гривны": 1.64, "Рубли": 1, "Киргизский сом": 0.76,
                    "Тенге": 0.13, "Узбекский сум": 0.0055, }
    currency_to_rub = {"Манаты": 35.68, "Белорусские рубли": 23.91, "Евро": 59.90, "Грузинский лари": 21.74,
                       "Киргизский сом": 0.76, "Тенге": 0.13, "Рубли": 1, "Гривны": 1.64, "Доллары": 60.66,
                       "Узбекский сум": 0.0055, }

    def test_sort_dict(self):
        self.assertEqual(self.result.sort_dict(self.currency_to_rub), self.correct_dict)


class DataSetTests(TestCase):
    dataset = tests.DataSet("vacancies.csv")

    def test_zero_length_str(self):
        count = 0

        for value in self.dataset.parsed_vacancies:
            if value == "":
                count += 1
        self.assertEqual(0, count)
