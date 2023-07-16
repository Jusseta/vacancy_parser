from src.api import HeadHunterAPI, SuperJobAPI
from src.vacancies import Vacancy, VacancyFile


def main():
    """Функция для взаимодействия с пользователем"""
    while True:
        keyword = input('Приветствую соискателей!\nВведите название вакансии или ключевое слово:\n')

        hh = HeadHunterAPI(keyword).get_response()
        sj = SuperJobAPI(keyword).get_response()
        if not hh and not sj:
            print('К сожалению, таких вакансий не обнаружено')
            exit()

        vf = VacancyFile()

        vf.add_to_file(hh, sj)

        currency = ''
        while currency == '':
            currency_input = int(input('Введите номер желаемой валюты:\n'
                                       '1 - RUB\n'
                                       '2 - USD\n'))
            if currency_input == 1:
                currency = 'rub'
            elif currency_input == 2:
                currency = 'usd'
            else:
                print('Нет такой валюты\n')
                continue

        salary = int(input('Введите минимальную желаемую зарплату\n'))

        vf.get_from_file(currency, salary)
        vac_lst = vf.vacancies
        if not vac_lst:
            print('Нет вакансий, соответствующих вашим желаниям')
            exit()

        choice = int(input('1 - Показать вакансии\n'
                           '2 - Выбрать занятость\n'))
        if choice == 1:
            None
        elif choice == 2:
            occupation = input('Какую занятость вы хотите иметь\n\n'
                               'Полная занятость\n'
                               'Частичная занятость\n'
                               'Стажировка\n'
                               'Проектная работу\n'
                               'Удаленная работу\n'
                               'Без разницы\n')

            if occupation == 'Без разницы':
                None
            else:
                vf.delete_from_file(occupation)

        sort = int(input('Отсортировать список вакансий?\n'
                         '1 - Вывести по умолчанию\n'
                         '2 - Отсортировать по зарплате (от большего к меньшему)\n'
                         '3 - Отсортировать по дате публикации (от нового к старому)\n'))

        fin_vac_lst = []
        if sort == 1:
            for vac in vac_lst:
                data = Vacancy(vac['platform'], vac['title'], vac['url'], vac['salary_from'],
                               vac['salary_to'], vac['date'], vac['employer'], vac['occupation'])
                fin_vac_lst.append(data)

        elif sort == 2:
            vf.sort_by_salary()
            vac_lst = vf.vacancies
            for vac in vac_lst:
                data = Vacancy(vac['platform'], vac['title'], vac['url'], vac['salary_from'],
                               vac['salary_to'], vac['date'], vac['employer'], vac['occupation'])
                fin_vac_lst.append(data)

        elif sort == 3:
            vf.sort_by_date()
            vac_lst = vf.vacancies
            for vac in vac_lst:
                data = Vacancy(vac['platform'], vac['title'], vac['url'], vac['salary_from'],
                               vac['salary_to'], vac['date'], vac['employer'], vac['occupation'])
                fin_vac_lst.append(data)

        if vac_lst:
            print(f'По вашему запросу найдено {len(fin_vac_lst)} вакансий')
        else:
            print('Нет вакансий, соответствующих вашим желаниям')

        number = 0
        for i in fin_vac_lst:
            number += 1
            print(f'№ {number}\n{i}')

        user = int(input('Желаете начать заново?\n'
                         '1 - Да\n'
                         '0 - Нет\n'))
        if user == 1:
            continue
        else:
            print('Всего хорошего!')
            exit()


if __name__ == '__main__':
    main()
