from abc import ABC, abstractmethod
import requests


class ApiAbc(ABC):
    url_get = "https://api.hh.ru/vacancies"

    @abstractmethod
    def check_status_request(self):
        pass

    @abstractmethod
    def get_answer(self):
        pass


class ApiHhVacancy(ApiAbc):
    quantity = 50

    def __init__(self, name_vacancy):
        self.name_vacancy = name_vacancy

    def check_status_request(self):
        response = requests.get(self.url_get)
        if response.ok is True:
            return True
        else:
            return False

    def get_answer(self):
        name = f'NAME:({self.name_vacancy})'
        parms = {"text": name, "per_page": self.quantity, "area": 1, "only_with_salary": True}
        response = requests.get(self.url_get, parms)
        return response.json()
