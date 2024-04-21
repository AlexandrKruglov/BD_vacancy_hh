import psycopg2
from typing import Any


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных ."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(50),
                employer_url text,
                quantity_vacancy INTEGER
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                vacancy_name VARCHAR(100) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                publish_date DATE,
                sity VARCHAR(50),
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()
    return True


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о компаниях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        temp = ''
        for i in data:
            items_list = i['items']
            if items_list[0]['employer']['name'] != temp:  #проверяем есть ли эта компания в таблице employers
                temp = items_list[0]['employer']['name']
                cur.execute(
                    """
                    INSERT INTO employers (employer_name, employer_url, quantity_vacancy)
                    VALUES (%s, %s, %s)
                    RETURNING employer_id
                    """,
                    (temp, items_list[0]['employer']['alternate_url'], i['found'])
                )
                employer_id = cur.fetchone()[0]
            for item in items_list:
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, vacancy_name, salary_from, salary_to, publish_date, sity, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (employer_id, item['name'], item['salary']['from'], item['salary']['to'], item['created_at'],
                     item['area']['name'],
                     item['alternate_url']))

    conn.commit()
    conn.close()
