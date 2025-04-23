import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from src.vacancy import Vacancy


class FileWorker(ABC):
    """
    Abstract class for file operations
    """

    def __init__(self, filename: str):
        """
        Initialize file worker
        """
        self._filename = filename

    @abstractmethod
    def add_vacancy(self, vacancy: Union[Vacancy, List[Vacancy]]) -> None:
        """
        Add vacancy or list of vacancies to file
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """
        Get vacancies from file, optionally filtered by criteria
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """
        Delete vacancy from file by ID
        """
        pass


class JSONSaver(FileWorker):
    """
    Class for working with JSON files to store vacancies
    """

    def __init__(self, filename: str = "vacancies.json"):
        """
        Initialize JSON file worker
        """
        super().__init__(filename)
        self.__ensure_file_exists()

    def __ensure_file_exists(self) -> None:
        """
        Ensure that the file exists, create if it doesn't
        """
        os.makedirs("data", exist_ok=True)

        filepath = os.path.join("data", self._filename)

        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def add_vacancy(self, vacancy: Union[Vacancy, List[Vacancy]]) -> None:
        """
        Add vacancy or list of vacancies to JSON file
        """
        filepath = os.path.join("data", self._filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                vacancies = json.load(f)
        except json.JSONDecodeError:
            vacancies = []

        if isinstance(vacancy, Vacancy):
            vacancies_to_add = [vacancy]
        else:
            vacancies_to_add = vacancy

        existing_ids = {v.get("id") for v in vacancies}

        for v in vacancies_to_add:
            if v.id not in existing_ids:
                vacancies.append(v.to_dict())
                existing_ids.add(v.id)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """
        Get vacancies from JSON file, optionally filtered by criteria
        """
        filepath = os.path.join("data", self._filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                vacancies = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

        vacancy_objects = [Vacancy.from_dict(v) for v in vacancies]

        if criteria:
            filtered_vacancies = []

            for vacancy in vacancy_objects:
                match = True

                for key, value in criteria.items():
                    if key == "keyword":
                        if (
                            value.lower() not in vacancy.name.lower()
                            and value.lower() not in vacancy.description.lower()
                        ):
                            match = False
                            break
                    elif key == "salary_from":
                        if vacancy.salary_from < value:
                            match = False
                            break
                    elif key == "salary_to":
                        if vacancy.salary_to > 0 and vacancy.salary_to > value:
                            match = False
                            break

                if match:
                    filtered_vacancies.append(vacancy)

            return filtered_vacancies

        return vacancy_objects

    def delete_vacancy(self, vacancy_id: str) -> None:
        """
        Delete vacancy from JSON file by ID
        """
        filepath = os.path.join("data", self._filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                vacancies = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return

        vacancies = [v for v in vacancies if v.get("id") != vacancy_id]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)
