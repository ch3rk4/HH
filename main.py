from src.api import HH
from src.file import JSONSaver
from src.vacancy import Vacancy
from src.utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, print_vacancies
import sys


def user_interaction(test_mode=False):
    """
    Function for user interaction through the console.
    Provides a command-line interface to search for vacancies on hh.ru,
    filter them by various criteria, and display information.

    Args:
        test_mode (bool): If True, exit after one menu action (for testing)
    """
    print("Приложение для поиска вакансий на hh.ru")
    print("=====================================")

    # Initialize file worker and API
    json_saver = JSONSaver()
    hh_api = HH(json_saver)

    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий")
        print("2. Получить топ-N вакансий по зарплате")
        print("3. Фильтр вакансий по ключевому слову")
        print("4. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            search_query = input("Введите поисковый запрос: ")

            try:
                print("Загрузка вакансий...")
                vacancies_data = hh_api.get_vacancies(search_query)

                if not vacancies_data:
                    print("Не найдено вакансий по вашему запросу.")
                    if test_mode: return
                    continue

                print(f"Найдено {len(vacancies_data)} вакансий.")

                # Convert to Vacancy objects
                vacancies = Vacancy.cast_to_object_list(vacancies_data)

                # Save to file
                json_saver.add_vacancy(vacancies)

                print("Вакансии успешно сохранены в файл.")

                # Ask if user wants to see results
                show = input("Показать найденные вакансии? (да/нет): ")
                if show.lower() == 'да':
                    top_n = int(input("Сколько вакансий показать? "))
                    top_vacancies = get_top_vacancies(sort_vacancies(vacancies), top_n)
                    print_vacancies(top_vacancies)

                if test_mode: return

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                if test_mode: return

        elif choice == '2':
            try:
                # Get all vacancies from file
                vacancies = json_saver.get_vacancies()

                if not vacancies:
                    print("В файле нет сохраненных вакансий. Сначала выполните поиск.")
                    if test_mode: return
                    continue

                top_n = int(input("Введите количество вакансий для вывода в топ N: "))

                # Sort and get top vacancies
                sorted_vacancies = sort_vacancies(vacancies)
                top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

                print_vacancies(top_vacancies)

                if test_mode: return

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                if test_mode: return

        elif choice == '3':
            try:
                # Get all vacancies from file
                vacancies = json_saver.get_vacancies()

                if not vacancies:
                    print("В файле нет сохраненных вакансий. Сначала выполните поиск.")
                    if test_mode: return
                    continue

                filter_keywords = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()

                # Filter vacancies
                filtered_vacancies = filter_vacancies(vacancies, filter_keywords)

                # Ask for salary range
                salary_range = input("Введите диапазон зарплат (например: 100000 - 150000) или оставьте пустым: ")

                if salary_range:
                    filtered_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

                # Print results
                print_vacancies(filtered_vacancies)

                if test_mode: return

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                if test_mode: return

        elif choice == '4':
            print("Спасибо за использование приложения!")
            sys.exit(0)

        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")
            if test_mode: return


if __name__ == "__main__":
    user_interaction()