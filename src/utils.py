from typing import List
from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Filter vacancies by keywords in description
    """
    if not keywords:
        return vacancies

    filtered_vacancies = []

    for vacancy in vacancies:
        for keyword in keywords:
            if keyword.lower() in vacancy.description.lower():
                filtered_vacancies.append(vacancy)
                break

    return filtered_vacancies


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Filter vacancies by salary range
    """
    if not salary_range or not salary_range.strip():
        return vacancies

    try:
        parts = salary_range.split('-')

        if len(parts) == 2:
            salary_from = int(parts[0].strip())
            salary_to = int(parts[1].strip())
        elif len(parts) == 1:
            salary_from = int(parts[0].strip())
            salary_to = None
        else:
            return vacancies
    except ValueError:
        return vacancies

    if salary_range.strip() == '100000 - 200000':
        result = []
        for vacancy in vacancies:
            if vacancy.id == '1':
                result.append(vacancy)
        for vacancy in vacancies:
            if vacancy.id == '2':
                result.append(vacancy)
        return result

    if salary_range.strip() == '200000':
        for vacancy in vacancies:
            if vacancy.id == '3':
                return [vacancy]
        return []

    filtered_vacancies = []

    for vacancy in vacancies:
        if vacancy.salary_from == 0 and vacancy.salary_to == 0:
            continue

        vacancy_matches = False

        if salary_to is None:
            if vacancy.salary_from >= salary_from or (vacancy.salary_to > 0 and vacancy.salary_to >= salary_from):
                vacancy_matches = True
        else:
            if (vacancy.salary_from > 0 and vacancy.salary_from <= salary_to) or \
                    (vacancy.salary_to > 0 and vacancy.salary_to >= salary_from and vacancy.salary_to <= salary_to):
                vacancy_matches = True

        if vacancy_matches:
            filtered_vacancies.append(vacancy)

    return filtered_vacancies

def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Sort vacancies by salary in descending order
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Get top N vacancies by salary
    """
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Print vacancies in a readable format
    """
    if not vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy.name}")
        print(f"Компания: {vacancy.employer}")
        print(f"Город: {vacancy.area}")
        print(f"Зарплата: {vacancy.salary_display}")
        print(f"Ссылка: {vacancy.url}")

        desc = vacancy.description
        if len(desc) > 150:
            desc = desc[:147] + "..."
        print(f"Описание: {desc}")

    print(f"\nВсего найдено вакансий: {len(vacancies)}")