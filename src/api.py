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


class HeadHunterAPI(AbstractAPI):
    '''Формирование запроса на HeadHunter'''
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


class SuperJobAPI(AbstractAPI):
    '''Формирование запроса на SuperJob'''
    def __init__(self, keyword: str):
        self.header = {'X-Api-App-Id': os.getenv('SuperJob_API_Key')}
        self.params = {'keyword': keyword, 'per_page': 100}

    def get_response(self):
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=self.header, params=self.params)
        if response.status_code != 200:
            raise ResponseError
        return response.json()['objects']
