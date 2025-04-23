import pytest
from unittest.mock import patch, MagicMock
import sys
import main
from src.vacancy import Vacancy


@pytest.fixture
def mock_vacancy():
    """Создание тестовой вакансии"""
    return Vacancy(
        vacancy_id='1',
        name='Python Developer',
        url='https://example.com/vacancy/1',
        salary={'from': 100000, 'to': 150000, 'currency': 'RUR'},
        description='Python, Django, Flask',
        employer='Test Company',
        area='Moscow'
    )


@pytest.fixture
def mock_vacancy_list(mock_vacancy):
    """Создание списка тестовых вакансий"""
    vacancy2 = Vacancy(
        vacancy_id='2',
        name='Senior Python Developer',
        url='https://example.com/vacancy/2',
        salary={'from': 200000, 'to': 250000, 'currency': 'RUR'},
        description='Python, Django, DRF',
        employer='Big Company',
        area='Saint Petersburg'
    )
    return [mock_vacancy, vacancy2]


def test_search_vacancies_success():
    """Тест успешного поиска вакансий"""
    # Создаем и настраиваем все необходимые моки
    mock_hh = MagicMock()
    mock_hh.get_vacancies.return_value = [{'id': '1'}, {'id': '2'}]

    mock_json_saver = MagicMock()

    mock_vacancy_list = [MagicMock(), MagicMock()]

    # Патчим все необходимые зависимости
    with patch('main.HH', return_value=mock_hh), \
            patch('main.JSONSaver', return_value=mock_json_saver), \
            patch('main.Vacancy.cast_to_object_list', return_value=mock_vacancy_list), \
            patch('main.sort_vacancies', return_value=mock_vacancy_list), \
            patch('main.get_top_vacancies', return_value=mock_vacancy_list), \
            patch('main.print_vacancies'), \
            patch('builtins.input', side_effect=['1', 'Python', 'да', '2']):
        # Запускаем функцию в тестовом режиме
        main.user_interaction(test_mode=True)

        # Проверяем, что были вызваны нужные методы
        mock_hh.get_vacancies.assert_called_once_with('Python')
        mock_json_saver.add_vacancy.assert_called_once_with(mock_vacancy_list)


def test_get_top_vacancies():
    """Тест получения топ-N вакансий по зарплате"""
    # Создаем и настраиваем моки
    mock_hh = MagicMock()
    mock_json_saver = MagicMock()
    mock_vacancy_list = [MagicMock(), MagicMock()]
    mock_json_saver.get_vacancies.return_value = mock_vacancy_list

    # Патчим зависимости
    with patch('main.HH', return_value=mock_hh), \
            patch('main.JSONSaver', return_value=mock_json_saver), \
            patch('main.sort_vacancies', return_value=mock_vacancy_list), \
            patch('main.get_top_vacancies', return_value=mock_vacancy_list), \
            patch('main.print_vacancies') as mock_print, \
            patch('builtins.input', side_effect=['2', '5']):
        # Запускаем функцию
        main.user_interaction(test_mode=True)

        # Проверяем вызовы
        mock_json_saver.get_vacancies.assert_called_once()
        mock_print.assert_called_once_with(mock_vacancy_list)


def test_filter_vacancies():
    """Тест фильтрации вакансий по ключевому слову"""
    # Создаем моки
    mock_hh = MagicMock()
    mock_json_saver = MagicMock()
    mock_vacancy_list = [MagicMock(), MagicMock()]
    mock_json_saver.get_vacancies.return_value = mock_vacancy_list

    # Патчим функции
    with patch('main.HH', return_value=mock_hh), \
            patch('main.JSONSaver', return_value=mock_json_saver), \
            patch('main.filter_vacancies', return_value=mock_vacancy_list) as mock_filter, \
            patch('main.get_vacancies_by_salary', return_value=mock_vacancy_list) as mock_salary, \
            patch('main.print_vacancies') as mock_print, \
            patch('builtins.input', side_effect=['3', 'Python Django', '100000 - 200000']):
        # Запускаем функцию
        main.user_interaction(test_mode=True)

        # Проверяем вызовы
        mock_json_saver.get_vacancies.assert_called_once()
        mock_filter.assert_called_once_with(mock_vacancy_list, ['Python', 'Django'])
        mock_salary.assert_called_once_with(mock_vacancy_list, '100000 - 200000')
        mock_print.assert_called_once_with(mock_vacancy_list)


def test_invalid_choice():
    """Тест ввода неверного пункта меню"""
    # Патчим зависимости
    with patch('main.HH'), \
            patch('main.JSONSaver'), \
            patch('builtins.print') as mock_print, \
            patch('builtins.input', return_value='10'):
        # Запускаем функцию
        main.user_interaction(test_mode=True)

        # Проверяем, что было выведено сообщение о неверном выборе
        mock_print.assert_any_call("Неверный выбор. Пожалуйста, выберите снова.")


def test_empty_vacancies():
    """Тест обработки пустого списка вакансий"""
    # Создаем моки
    mock_hh = MagicMock()
    mock_json_saver = MagicMock()
    mock_json_saver.get_vacancies.return_value = []

    # Патчим функции
    with patch('main.HH', return_value=mock_hh), \
            patch('main.JSONSaver', return_value=mock_json_saver), \
            patch('builtins.print') as mock_print, \
            patch('builtins.input', return_value='2'):
        # Запускаем функцию
        main.user_interaction(test_mode=True)

        # Проверяем, что было выведено сообщение об отсутствии вакансий
        mock_print.assert_any_call("В файле нет сохраненных вакансий. Сначала выполните поиск.")


def test_api_error():
    """Тест обработки ошибки API"""
    # Создаем моки
    mock_hh = MagicMock()
    mock_hh.get_vacancies.side_effect = Exception("API Error")
    mock_json_saver = MagicMock()

    # Патчим функции
    with patch('main.HH', return_value=mock_hh), \
            patch('main.JSONSaver', return_value=mock_json_saver), \
            patch('builtins.print') as mock_print, \
            patch('builtins.input', side_effect=['1', 'Python']):
        # Запускаем функцию
        main.user_interaction(test_mode=True)

        # Проверяем, что было выведено сообщение об ошибке
        mock_print.assert_any_call("Произошла ошибка: API Error")