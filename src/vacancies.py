from abc import ABC, abstractmethod
import json
from datetime import datetime
import datetime


class Vacancy:
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
    def __init__(self):
        self.file_name = 'vacancies.json'
        self.vacancies = []

    def add_to_file(self, hh_vacancies: list, sj_vacancies: list):
        with open(f'hh_{self.file_name}', 'w', encoding='utf-8') as file:
            json.dump(hh_vacancies, file, ensure_ascii=False, indent=4)
        with open(f'sj_{self.file_name}', 'w', encoding='utf-8') as file:
            json.dump(sj_vacancies, file, ensure_ascii=False, indent=4)

    def get_from_file(self, currency: str, salary: int):

        with open(f'hh_{self.file_name}', 'r', encoding='utf-8') as file:
            hh_data = json.load(file)
            hh_vacancies = []

            if currency == 'rub':
                currency = 'rur'

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

                                hh_vacancies.append(data)

        with open(f'sj_{self.file_name}', 'r', encoding='utf-8') as file:
            sj_data = json.load(file)
            sj_vacancies = []

            for vac in sj_data:
                if vac['payment_from'] >= salary:
                    salary_from = vac['payment_from']
                    salary_to = vac['payment_to'] if vac['payment_to'] != 0 else 'Не указано'

                    if vac['currency'] == currency.lower():

                        date_raw = vac['date_published']
                        date_published = datetime.datetime.fromtimestamp(date_raw)
                        date = date_published.strftime('%Y-%m-%d %H:%M:%S')

                        data = {
                            'platform': 'SuperJob',
                            'title': vac['profession'],
                            'url': vac['link'],
                            'salary_from': salary_from,
                            'salary_to': salary_to,
                            'date': date,
                            'employer': vac['firm_name']
                                }

                        sj_vacancies.append(data)

        self.vacancies = hh_vacancies + sj_vacancies

    def delete_from_file(self, keyword):
        with open(f'sj_{self.file_name}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for i in reversed(range(len(data))):
                if keyword.casefold() in data[i]['place_of_work']['title']:
                    del data[i]

            with open(f'sj_{self.file_name}', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        with open(f'hh_{self.file_name}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for i in reversed(range(len(data))):
                if keyword.casefold() in data[i]['employment']['name']:
                    del data[i]

            with open(f'hh_{self.file_name}', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def sort_by_salary(self):
        vacancies = self.vacancies.sort(key=lambda k: k['salary_from'], reverse=True)
        return vacancies

    def sort_by_date(self):
        vacancies = self.vacancies.sort(key=lambda k: k['date'], reverse=True)
        return vacancies
