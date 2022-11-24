import vacancies
import statistic

inputed = input("Напишите слово Вакансии или Статистика: ")

if inputed == "Вакансии":
    vacancies.Initialization()
elif inputed == "Статистика":
    statistic.Initialization()
else:
<<<<<<< develop
    print("Вы ввели неправильно")
=======
    print("Вы ввели неправильно текст")
>>>>>>> local
