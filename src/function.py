import requests
from db_manager_class import DBManager


def get_data_at_api(url_get: str, employers_id):
    """" функция для работы с api. возвращает данные по запросу"""
    data_list = []
    for i in employers_id:
        num_page = 0
        while True:
            parms = {"page": num_page, "employer_id": i, "only_with_salary": True}
            response = requests.get(url_get, parms)
            a = response.json()
            data_list.append(a)
            num_page += 1
            if num_page < a["pages"] and num_page < 10:  #вывод ограничен 10 страницами
                continue
            else:
                break
    return data_list

def str_data (data):
    """Функция для вывода инф. о вакансии в удобном виде"""
    for i in data:
        print(f"компания:{i[0]}, {i[1]},  город: {i[2]},  зарплата {i[3]} - {i[4]},   url - {i[5]}")

def conect_whith_user():
    """Функция для общения пользователя с Б.Д."""
    print("создана база данных с вакансиями hh_vacancy")
    print("в ней находятся  :")
    exampl = DBManager("hh_vacancy")
    employer = exampl.get_companies_and_vacancies_count()
    for i in employer:
        print(f"компания: {i[0]} - {i[1]} вакансий ")
    while True:
        print("Вы можете получаеть список всех вакансий набрав -- all")
        print("Вы можете получает среднюю зарплату по вакансиям  набрав -- avg")
        print("Вы можете получает список всех вакансий, у которых зарплата выше средней по всем вакансиям набрав -- max")
        print("Вы можете получает список всех вакансий, в названии которых содержатся искомые слова  набрав -- search")
        item = input("  :: ")
        if item == "all":
            str_data(exampl.get_all_vacancies())
        elif item == "avg":
            print(exampl.get_avg_salary())
        elif item == "max":
            str_data(exampl.get_vacancies_with_higher_salary())
        elif item == "search":
            str_data(exampl.get_vacancies_with_keyword())
        print("\nпродолжить работу нажмите д\n"
              "закончить работу нажмите любую букву")
        temp = input()
        if temp == "д":
            continue
        print("досвидания")
        break

