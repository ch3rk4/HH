from typing import Any, Dict, List, Optional


class Vacancy:
    """
    Class for working with vacancy data
    """

    __slots__ = (
        "__id",
        "__name",
        "__url",
        "__salary",
        "__description",
        "__employer",
        "__area",
    )

    def __init__(
        self,
        vacancy_id: str,
        name: str,
        url: str,
        salary: Optional[Dict[str, Any]],
        description: str,
        employer: str,
        area: str,
    ):
        """
        Initialize vacancy with data
        """
        self.__id = vacancy_id
        self.__name = name
        self.__url = url
        self.__salary = self.__validate_salary(salary)
        self.__description = description
        self.__employer = employer
        self.__area = area

    def __validate_salary(self, salary: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate and normalize salary data
        """
        if not salary:
            return {
                "from": 0,
                "to": 0,
                "currency": "RUR",
                "display": "Зарплата не указана",
            }

        result = {
            "from": salary.get("from", 0) or 0,
            "to": salary.get("to", 0) or 0,
            "currency": salary.get("currency", "RUR"),
        }

        if result["from"] and result["to"]:
            result["display"] = (
                f"{result['from']} - {result['to']} {result['currency']}"
            )
        elif result["from"]:
            result["display"] = f"от {result['from']} {result['currency']}"
        elif result["to"]:
            result["display"] = f"до {result['to']} {result['currency']}"
        else:
            result["display"] = "Зарплата не указана"

        return result

    @property
    def id(self) -> str:
        """Get vacancy ID"""
        return self.__id

    @property
    def name(self) -> str:
        """Get vacancy name"""
        return self.__name

    @property
    def url(self) -> str:
        """Get vacancy URL"""
        return self.__url

    @property
    def salary(self) -> Dict[str, Any]:
        """Get salary information dictionary"""
        return self.__salary

    @property
    def description(self) -> str:
        """Get vacancy description"""
        return self.__description

    @property
    def employer(self) -> str:
        """Get employer name"""
        return self.__employer

    @property
    def area(self) -> str:
        """Get work area (city/region)"""
        return self.__area

    @property
    def salary_from(self) -> int:
        """Get minimum salary"""
        return self.__salary["from"]

    @property
    def salary_to(self) -> int:
        """Get maximum salary"""
        return self.__salary["to"]

    @property
    def salary_currency(self) -> str:
        """Get salary currency"""
        return self.__salary["currency"]

    @property
    def salary_display(self) -> str:
        """Get formatted salary string for display"""
        return self.__salary["display"]

    def __lt__(self, other) -> bool:
        """
        Compare vacancies by salary_from (less than)
        """
        if not isinstance(other, Vacancy):
            return NotImplemented

        if self.salary_from == 0 and other.salary_from == 0:
            return self.salary_to < other.salary_to

        if self.salary_from == 0:
            return True

        if other.salary_from == 0:
            return False

        return self.salary_from < other.salary_from

    def __le__(self, other) -> bool:
        """Less than or equal comparison"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self < other or self == other

    def __gt__(self, other) -> bool:
        """Greater than comparison"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return not (self < other or self == other)

    def __ge__(self, other) -> bool:
        """Greater than or equal comparison"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return not self < other

    def __eq__(self, other) -> bool:
        """Equal comparison (based on vacancy ID)"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.__id == other.__id

    def __ne__(self, other) -> bool:
        """Not equal comparison"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return not self == other

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert vacancy to dictionary for serialization
        """
        return {
            "id": self.__id,
            "name": self.__name,
            "url": self.__url,
            "salary": self.__salary,
            "description": self.__description,
            "employer": self.__employer,
            "area": self.__area,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """
        Create vacancy from dictionary (deserialization)
        """
        return cls(
            vacancy_id=data["id"],
            name=data["name"],
            url=data["url"],
            salary=data["salary"],
            description=data["description"],
            employer=data["employer"],
            area=data["area"],
        )

    @staticmethod
    def cast_to_object_list(vacancies_data: List[Dict[str, Any]]) -> List["Vacancy"]:
        """
        Convert list of dictionaries from API to list of Vacancy objects
        """
        vacancy_objects = []

        for vacancy_dict in vacancies_data:
            snippet = vacancy_dict.get("snippet", {})
            employer = vacancy_dict.get("employer", {})
            area = vacancy_dict.get("area", {})

            requirement = snippet.get("requirement", "")
            responsibility = snippet.get("responsibility", "")
            description = f"{requirement} {responsibility}".strip()

            vacancy = Vacancy(
                vacancy_id=vacancy_dict.get("id", ""),
                name=vacancy_dict.get("name", ""),
                url=vacancy_dict.get("alternate_url", ""),
                salary=vacancy_dict.get("salary"),
                description=description,
                employer=employer.get("name", ""),
                area=area.get("name", ""),
            )

            vacancy_objects.append(vacancy)

        return vacancy_objects
