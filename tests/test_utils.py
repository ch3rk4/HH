import pytest

from src.utils import (filter_vacancies, get_top_vacancies,
                       get_vacancies_by_salary, print_vacancies,
                       sort_vacancies)
from src.vacancy import Vacancy


class TestUtils:
    @pytest.fixture
    def vacancies(self):
        """Fixture for a list of test vacancies"""
        return [
            Vacancy(
                vacancy_id="1",
                name="Junior Python Developer",
                url="https://example.com/1",
                salary={"from": 80000, "to": 100000, "currency": "RUR"},
                description="Python, Django, entry-level position",
                employer="Company A",
                area="Moscow",
            ),
            Vacancy(
                vacancy_id="2",
                name="Middle Python Developer",
                url="https://example.com/2",
                salary={"from": 150000, "to": 200000, "currency": "RUR"},
                description="Python, Flask, SqlAlchemy, 2+ years experience",
                employer="Company B",
                area="Saint Petersburg",
            ),
            Vacancy(
                vacancy_id="3",
                name="Senior Python Developer",
                url="https://example.com/3",
                salary={"from": 250000, "to": 300000, "currency": "RUR"},
                description="Python, Django, DRF, team lead experience",
                employer="Company C",
                area="Moscow",
            ),
            Vacancy(
                vacancy_id="4",
                name="Java Developer",
                url="https://example.com/4",
                salary={"from": 180000, "to": 220000, "currency": "RUR"},
                description="Java, Spring, Hibernate",
                employer="Company D",
                area="Kazan",
            ),
            Vacancy(
                vacancy_id="5",
                name="Frontend Developer",
                url="https://example.com/5",
                salary=None,
                description="JavaScript, React, Redux",
                employer="Company E",
                area="Remote",
            ),
        ]

    def test_filter_vacancies(self, vacancies):
        """Test filtering vacancies by keywords"""
        filtered = filter_vacancies(vacancies, ["Python"])
        assert len(filtered) == 3
        assert filtered[0].id == "1"
        assert filtered[1].id == "2"
        assert filtered[2].id == "3"

        filtered = filter_vacancies(vacancies, ["Django"])
        assert len(filtered) == 2
        assert filtered[0].id == "1"
        assert filtered[1].id == "3"

        filtered = filter_vacancies(vacancies, ["Java", "JavaScript"])
        assert len(filtered) == 2
        assert filtered[0].id == "4"
        assert filtered[1].id == "5"

        filtered = filter_vacancies(vacancies, ["Golang"])
        assert len(filtered) == 0

        filtered = filter_vacancies(vacancies, [])
        assert len(filtered) == 5

    def test_get_vacancies_by_salary(self, vacancies):
        """Test filtering vacancies by salary range"""
        filtered = get_vacancies_by_salary(vacancies, "100000 - 200000")
        assert len(filtered) == 2
        assert filtered[0].id == "1"
        assert filtered[1].id == "2"

        filtered = get_vacancies_by_salary(vacancies, "200000")
        assert len(filtered) == 1
        assert filtered[0].id == "3"

        filtered = get_vacancies_by_salary(vacancies, "invalid")
        assert len(filtered) == 5

        filtered = get_vacancies_by_salary(vacancies, "")
        assert len(filtered) == 5

    def test_sort_vacancies(self, vacancies):
        """Test sorting vacancies by salary"""
        sorted_vacancies = sort_vacancies(vacancies)

        assert sorted_vacancies[0].id == "3"
        assert sorted_vacancies[1].id == "4"
        assert sorted_vacancies[2].id == "2"
        assert sorted_vacancies[3].id == "1"
        assert sorted_vacancies[4].id == "5"

    def test_get_top_vacancies(self, vacancies):
        """Test getting top N vacancies"""
        sorted_vacancies = sort_vacancies(vacancies)

        top_3 = get_top_vacancies(sorted_vacancies, 3)
        assert len(top_3) == 3
        assert top_3[0].id == "3"
        assert top_3[1].id == "4"
        assert top_3[2].id == "2"

        top_1 = get_top_vacancies(sorted_vacancies, 1)
        assert len(top_1) == 1
        assert top_1[0].id == "3"

        top_10 = get_top_vacancies(sorted_vacancies, 10)
        assert len(top_10) == 5

    def test_print_vacancies(self, vacancies, capsys):
        """Test printing vacancies to console"""
        print_vacancies([vacancies[0]])
        captured = capsys.readouterr()

        assert "1. Junior Python Developer" in captured.out
        assert "Компания: Company A" in captured.out
        assert "Город: Moscow" in captured.out
        assert "Зарплата: 80000 - 100000 RUR" in captured.out
        assert "Описание: Python, Django, entry-level position" in captured.out

        print_vacancies([])
        captured = capsys.readouterr()
        assert "Нет вакансий" in captured.out
