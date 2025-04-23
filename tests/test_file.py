from unittest.mock import mock_open, patch

import pytest

from src.file import JSONSaver
from src.vacancy import Vacancy


class TestJSONSaver:
    @pytest.fixture
    def vacancy(self):
        """Fixture for a test vacancy"""
        return Vacancy(
            vacancy_id="1",
            name="Test Vacancy",
            url="https://example.com",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Test description",
            employer="Test Employer",
            area="Test Area",
        )

    @pytest.fixture
    def json_saver(self):
        """Fixture for a JSONSaver instance with test filename"""
        return JSONSaver(filename="test_vacancies.json")

    def test_add_vacancy_single(self, vacancy, json_saver):
        """Test adding a single vacancy to file"""
        with patch("os.path.exists", return_value=True), patch("os.makedirs"), patch(
            "builtins.open", mock_open(read_data="[]")
        ), patch("json.dump") as mock_dump, patch("json.load", return_value=[]):
            json_saver.add_vacancy(vacancy)

            called_args = mock_dump.call_args[0]
            assert len(called_args) >= 1
            assert len(called_args[0]) == 1
            assert called_args[0][0]["id"] == "1"

    def test_add_vacancy_list(self, vacancy, json_saver):
        """Test adding multiple vacancies to file"""
        vacancy2 = Vacancy(
            vacancy_id="2",
            name="Another Vacancy",
            url="https://example.com/2",
            salary={"from": 200000, "currency": "RUR"},
            description="Another description",
            employer="Another Employer",
            area="Another Area",
        )

        with patch("os.path.exists", return_value=True), patch("os.makedirs"), patch(
            "builtins.open", mock_open(read_data="[]")
        ), patch("json.dump") as mock_dump, patch("json.load", return_value=[]):
            json_saver.add_vacancy([vacancy, vacancy2])

            called_args = mock_dump.call_args[0]
            assert len(called_args) >= 1
            assert len(called_args[0]) == 2
            assert called_args[0][0]["id"] == "1"
            assert called_args[0][1]["id"] == "2"

    def test_get_vacancies_no_criteria(self, vacancy, json_saver):
        """Test getting vacancies without filtering criteria"""
        vacancy_dict = vacancy.to_dict()

        with patch("os.path.exists", return_value=True), patch("os.makedirs"), patch(
            "builtins.open", mock_open()
        ), patch("json.load", return_value=[vacancy_dict]):
            vacancies = json_saver.get_vacancies()

            assert len(vacancies) == 1
            assert vacancies[0].id == "1"
            assert vacancies[0].name == "Test Vacancy"

    def test_get_vacancies_with_keyword(self, vacancy, json_saver):
        """Test getting vacancies with keyword filter"""
        vacancy_dict = vacancy.to_dict()

        with patch("os.path.exists", return_value=True), patch("os.makedirs"), patch(
            "builtins.open", mock_open()
        ), patch("json.load", return_value=[vacancy_dict]):
            vacancies = json_saver.get_vacancies({"keyword": "Test"})

            assert len(vacancies) == 1

            vacancies = json_saver.get_vacancies({"keyword": "NonExistent"})
            assert len(vacancies) == 0

    def test_delete_vacancy(self, vacancy, json_saver):
        """Test deleting a vacancy by ID"""
        vacancy_dict = vacancy.to_dict()

        with patch("os.path.exists", return_value=True), patch("os.makedirs"), patch(
            "builtins.open", mock_open()
        ), patch("json.load", return_value=[vacancy_dict]), patch(
            "json.dump"
        ) as mock_dump:
            json_saver.delete_vacancy("1")

            called_args = mock_dump.call_args[0]
            assert len(called_args) >= 1
            assert len(called_args[0]) == 0
