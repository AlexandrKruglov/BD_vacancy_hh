import psycopg2


class DBManager():
    """классдля работы с Б.Д."""
    params = {'host': 'localhost',
              'user': 'postgres',
              'password': 12345,
              'port': 5432}

    def __init__(self, database_name: str):
        self.database_name = database_name

    def get_companies_and_vacancies_count(self):
        "получает список всех компаний и количество вакансий у каждой компании."
        params = self.params
        with psycopg2.connect(dbname=self.database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                       select DISTINCT employer_name, quantity_vacancy from employers
                   """)
                data = cur.fetchall()
        conn.commit()
        conn.close()
        return data

    def get_all_vacancies(self):
        "получает список всех вакансий с указанием названия компании,названия вакансии и зарплаты и ссылки на вакансию."
        params = self.params
        with psycopg2.connect(dbname=self.database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                               SELECT employer_name, vacancy_name, sity, salary_from, salary_to, vacancy_url  FROM employers
                               INNER JOIN vacancies USING(employer_id)
                           """)
                data = cur.fetchall()
        conn.commit()
        conn.close()
        return data

    def get_avg_salary(self):
        "получает среднюю зарплату по вакансиям."
        params = self.params
        with psycopg2.connect(dbname=self.database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT (AVG (salary_from)+ AVG(salary_to))/2 FROM vacancies
                                   """)
                data = cur.fetchall()
        conn.commit()
        conn.close()
        n_data = data[0][0]
        return int(n_data)

    def get_vacancies_with_higher_salary(self):
        " — получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."
        params = self.params
        with psycopg2.connect(dbname=self.database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                 SELECT (AVG (salary_from)+ AVG(salary_to))/2 FROM vacancies
                                       """)
                data = cur.fetchall()
                cur.execute(
                    f"SELECT employer_name, vacancy_name, sity, salary_from, salary_to, vacancy_url  FROM vacancies "
                    f"INNER JOIN employers USING(employer_id) "
                    f"WHERE salary_from > {data[0][0]} OR salary_to > {data[0][0]}")
                new_data = cur.fetchall()
        conn.commit()
        conn.close()
        return new_data

    def get_vacancies_with_keyword(self):
        " получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."
        params = self.params
        with psycopg2.connect(dbname=self.database_name, **params) as conn:
            with conn.cursor() as cur:
                while True:
                    word = input("Введите слово для поиска : ")
                    new_word = word.title()
                    cur.execute(
                        f"SELECT employer_name, vacancy_name, sity, salary_from, salary_to, vacancy_url  FROM vacancies "
                        f"INNER JOIN employers USING(employer_id) "
                        f"WHERE vacancy_name LIKE '%{word}%'"
                    )
                    data = cur.fetchall()
                    cur.execute(
                        f"SELECT employer_name, vacancy_name, sity, salary_from, salary_to, vacancy_url  FROM vacancies "
                        f"INNER JOIN employers USING(employer_id) "
                        f"WHERE vacancy_name LIKE '%{new_word}%'"
                    )
                    new_data = cur.fetchall()
                    data = data + new_data
                    if len(data) == 0:
                        print("Нет ваконсий по данному запросу. Ведите -да- для повторного поиска.,"
                              " или любую букву для завершения. ")
                        letter = input(": ")
                        if letter == "да":
                            continue
                        break
                    break
        conn.commit()
        conn.close()
        return data
