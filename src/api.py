from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class Parser(ABC):
    """
    Abstract class for API parsers that defines the interface for all parser classes.
    """

    def __init__(self, file_worker):
        """
        Initialize parser with a file worker instance
        """
        self.file_worker = file_worker

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Get vacancies from API by keyword
        """
        pass

    @abstractmethod
    def _connect(self) -> None:
        """
        Connect to API to check availability
        """
        pass


class HH(Parser):
    """
    Class for working with HeadHunter API
    """

    def __init__(self, file_worker):
        """
        Initialize HeadHunter API parser
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []
        super().__init__(file_worker)

    def _connect(self) -> None:
        """
        Connect to HeadHunter API to check availability
        """
        response = requests.get(self.__url, headers=self.__headers)
        if response.status_code != 200:
            raise ConnectionError(
                f"Failed to connect to HH API: {response.status_code}"
            )

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Get vacancies from HeadHunter API by keyword
        """
        self._connect()

        self.__params["text"] = keyword
        self.__vacancies = []

        page = 0
        total_pages = 20

        while page < total_pages:
            self.__params["page"] = page
            response = requests.get(
                self.__url, headers=self.__headers, params=self.__params
            )
            data = response.json()

            if not data.get("items"):
                break

            self.__vacancies.extend(data["items"])
            page += 1

            if page >= data.get("pages", 0):
                break

        return self.__vacancies
