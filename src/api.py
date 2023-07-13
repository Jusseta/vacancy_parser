from abc import ABC, abstractmethod
import requests
import os


class ResponseError(Exception):
    def __init__(self):
        self.message = 'Проблема соединения с сервером'

    def __str__(self):
        return self.message


class AbstractAPI(ABC):
    @abstractmethod
    def get_response(self):
        pass

    def get_vacancies(self, currency: str, salary: int):
        pass


class HeadHunterAPI(AbstractAPI):
    def __init__(self, keyword: str):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.params = {'text': keyword, 'per_page': 100}

    def get_response(self):
        response = requests.get('https://api.hh.ru/vacancies', headers=self.header, params=self.params)
        if response.status_code != 200:
            raise ResponseError

        return response.json()['items']

    def get_vacancies(self, currency: str, salary: int):
        vacancies = []
        for vac in self.get_response():
            if vac['salary'] and vac['salary']['currency']:
                if vac['salary']['currency'] == currency.upper() and vac['salary']['from']:
                    if vac['salary']['from'] >= salary:
                        data = {
                            'title': vac['name'],
                            'url': 'https://hh.ru/vacancy/' + vac['id'],
                            'salary_currency': vac['salary']['currency'],
                            'salary_from': vac['salary']['from'],
                            'salary_to': vac['salary']['to'],
                            'date': vac['published_at'],
                            'employer': vac['employer']['name']
                        }
                        vacancies.append(data)
        return vacancies


class SuperJobAPI(AbstractAPI):
    def __init__(self, keyword: str):
        self.header = {'X-Api-App-Id': os.getenv('SuperJob_API_Key')}
        self.params = {'keyword': keyword, 'per_page': 100}

    def get_response(self):
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=self.header, params=self.params)
        if response.status_code != 200:
            raise ResponseError
        return response.json()['objects']

    def get_vacancies(self, currency: str, salary: int):
        vacancies = []
        for vac in self.get_response():
            if vac['payment_from'] >= salary and vac['currency'] == currency.lower():
                data = {
                    'title': vac['profession'],
                    'url': vac['link'],
                    'salary_currency': vac['currency'],
                    'salary_from': vac['payment_from'],
                    'salary_to': vac['payment_to'],
                    'date': vac['date_published'],
                    'employer': vac['firm_name']
                }
                vacancies.append(data)
        return vacancies
