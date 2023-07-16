from abc import ABC, abstractmethod
import json
from datetime import datetime
import datetime


class Vacancy:
    """Класс для инициализации вакансий"""
    def __init__(self, platform, title, url, salary_from, salary_to, date, employer):
        self.platform = platform
        self.title = title
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.date = date
        self.employer = employer

    def __str__(self):
        return f"Сайт: {self.platform}\n" \
               f"Вакансия: {self.title}\n" \
               f"Зарплата: от {self.salary_from} до {self.salary_to},\n" \
               f"Работодатель: {self.employer},\n" \
               f"Дата публикации: {self.date},\n" \
               f"Ссылка: {self.url}\n"

    def __eq__(self, other):
        return self.salary_from == other.salary_from

    def __le__(self, other):
        return self.salary_from <= other.salary_from

    def __ge__(self, other):
        return self.salary_from >= other.salary_from


class AbstractVacancyFile(ABC):

    @abstractmethod
    def add_to_file(self, hh_vacancies: list, sj_vacancies: list):
        pass

    @abstractmethod
    def get_from_file(self, currency: str, salary: int):
        pass

    @abstractmethod
    def delete_from_file(self, keyword):
        pass


class VacancyFile(AbstractVacancyFile):
    """Класс для добавления вакансий в json файл и работы с ним"""
    def __init__(self):
        self.file_name = 'vacancies.json'
        self.vacancies = []

    def add_to_file(self, hh_vacancies: list, sj_vacancies: list):
        """
        Добавляет вакансии в json файл
        :param hh_vacancies: список вакансий с HH
        :param sj_vacancies: список вакансий с SJ
        :return: None
        """
        with open(f'hh_{self.file_name}', 'w', encoding='utf-8') as file:
            json.dump(hh_vacancies, file, ensure_ascii=False, indent=4)
        with open(f'sj_{self.file_name}', 'w', encoding='utf-8') as file:
            json.dump(sj_vacancies, file, ensure_ascii=False, indent=4)

    def get_from_file(self, currency: str, salary: int):
        """
        Читает json файл и обавляет в список vacancies подходящие словари
        :param currency: валюта
        :param salary: минимальная зарплата
        :return: None
        """
        with open(f'sj_{self.file_name}', 'r', encoding='utf-8') as file:
            sj_data = json.load(file)

            if sj_data:
                for vac in sj_data:
                    if vac['payment_from'] >= salary:
                        salary_from = vac['payment_from']
                        salary_to = vac['payment_to'] if vac['payment_to'] != 0 else 'Не указано'

                        if vac['currency'] == currency.lower():
                            date_raw = vac['date_published']
                            date_published = datetime.datetime.fromtimestamp(date_raw)
                            date = date_published.strftime('%d.%m.%Y')

                            data = {
                                'platform': 'SuperJob',
                                'title': vac['profession'],
                                'url': vac['link'],
                                'salary_from': salary_from,
                                'salary_to': salary_to,
                                'date': date,
                                'employer': vac['firm_name']
                            }

                            self.vacancies.append(data)

        with open(f'hh_{self.file_name}', 'r', encoding='utf-8') as file:
            hh_data = json.load(file)

            if currency == 'rub':
                currency = 'rur'

            if hh_data:
                for vac in hh_data:
                    if vac['salary'] and vac['salary']['from']:
                        if vac['salary']['from'] >= salary:
                            salary_from = vac['salary']['from']
                            salary_to = vac['salary']['to'] if vac['salary']['to'] else 'Не указано'

                            if vac['salary']['currency']:
                                if vac['salary']['currency'] == currency.upper():
                                    raw_date = vac['published_at']
                                    date = datetime.datetime.fromisoformat(raw_date).strftime('%d.%m.%Y')
                                    data = {
                                        'platform': 'HeadHunter',
                                        'title': vac['name'],
                                        'url': 'https://hh.ru/vacancy/' + vac['id'],
                                        'salary_from': salary_from,
                                        'salary_to': salary_to,
                                        'date': date,
                                        'employer': vac['employer']['name']
                                            }

                                    self.vacancies.append(data)

    def delete_from_file(self, keyword):
        """
        Удаляет из json файла неподходящие по занятости вакансии
        :param keyword: занятость
        :return: None
        """
        with open(f'sj_{self.file_name}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for i in reversed(range(len(data))):
                if keyword.title() in data[i]['place_of_work']['title']:
                    del data[i]

            with open(f'sj_{self.file_name}', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        with open(f'hh_{self.file_name}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for i in reversed(range(len(data))):
                if keyword.title() in data[i]['employment']['name']:
                    del data[i]

            with open(f'hh_{self.file_name}', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def sort_by_salary(self):
        """Сортирует список vacancies по зарплате (от большего к меньшему)"""
        vacancies = self.vacancies.sort(key=lambda k: k['salary_from'], reverse=True)
        return vacancies

    def sort_by_date(self):
        """Сортирует список vacancies по дате (от новых к старым)"""
        vacancies = self.vacancies.sort(key=lambda k: k['date'], reverse=True)
        return vacancies
