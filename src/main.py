from src.db_create import create_database, save_data_to_database
from src.function import get_data_at_api, conect_whith_user

url_get = "https://api.hh.ru/vacancies"
employers_id = ["15478", "1740", "5779602", "9498112", "3776", "829010", "2180"]  # список компаний
params = {'host': 'localhost',
          'user': 'postgres',
          'password': 12345,
          'port': 5432}


def main():
    data_list = get_data_at_api(url_get, employers_id)  # получаем данные от сайта
    create_database("hh_vacancy", params)  # создаем базу данных с таблицами
    save_data_to_database(data_list, "hh_vacancy", params)  # заполняем таблицы данными
    conect_whith_user()  # функция для общения с полбзователем

if __name__ == '__main__':
    main()