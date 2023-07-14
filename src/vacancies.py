from abc import ABC, abstractmethod
import json
from datetime import datetime


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
                   f"Дата публикации: {date},\n" \
                   f"Ссылка: {self.url}"

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


class VacancyFile(AbstractVacancyFile):
    def __init__(self):
        self.file_name = 'vacancies.json'

    def add_to_file(self, hh_vacancies: list, sj_vacancies: list):
        with open(f'hh_{self.file_name}', 'w', encoding='utf-8') as file:
            json.dump(hh_vacancies, file, ensure_ascii=False, indent=4)
        with open(f'sj_{self.file_name}', 'w', encoding='utf-8') as file:
            json.dump(sj_vacancies, file, ensure_ascii=False, indent=4)

    def get_from_file(self, currency: str, salary: int):
        with open(f'hh_{self.file_name}', 'r', encoding='utf-8') as file:
            hh_data = json.load(file)
            hh_vacancies = []

            for vac in hh_data:
                if vac['salary']:
                    salary_from = vac['salary']['from'] if vac['salary']['from'] else 'Не указано'
                    salary_to = vac['salary']['to'] if vac['salary']['to'] else 'Не указано'

                    if vac['salary']['currency']:
                        if vac['salary']['currency'] == currency.upper():
                            date = datetime.fromisoformat(vac['published_at']).strftime('%d.%m.%Y')
                            data = Vacancy('HeadHunter',
                                           vac['name'],
                                           'https://hh.ru/vacancy/' + vac['id'],
                                           salary_from,
                                           salary_to,
                                           date,
                                           vac['employer']['name'])

                            hh_vacancies.append(data)

        with open(f'sj_{self.file_name}', 'r', encoding='utf-8') as file:
            sj_data = json.load(file)
            sj_vacancies = []

            for vac in sj_data:
                salary_from = vac['payment_from'] if vac['payment_from'] != 0 else 'Не указано'
                salary_to = vac['payment_to'] if vac['payment_to'] != 0 else 'Не указано'

                if vac['currency'] == currency:
                    data = Vacancy('SuperJob',
                                   vac['profession'],
                                   vac['link'],
                                   salary_from,
                                   salary_to,
                                   vac['date_published'],
                                   vac['firm_name'])

                    sj_vacancies.append(data)

        vacancies = hh_vacancies + sj_vacancies

        return vacancies
