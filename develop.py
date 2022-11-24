import vacancies
import statistic

inputed = input("Напишите слово Вакансии или Статистика: ")

if inputed == "Вакансии":
    vacancies.Initialization()
elif inputed == "Статистика":
    statistic.Initialization()
else:
    print("Вы ввели неправильно что-то")