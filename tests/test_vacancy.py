from src.vacancy import Vacancy


class TestVacancy:
    def test_init_with_salary(self):
        """Test vacancy initialization with salary data"""
        vacancy = Vacancy(
            vacancy_id="1",
            name="Test Vacancy",
            url="https://example.com",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Test description",
            employer="Test Employer",
            area="Test Area",
        )

        assert vacancy.id == "1"
        assert vacancy.name == "Test Vacancy"
        assert vacancy.url == "https://example.com"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.salary_currency == "RUR"
        assert vacancy.salary_display == "100000 - 150000 RUR"
        assert vacancy.description == "Test description"
        assert vacancy.employer == "Test Employer"
        assert vacancy.area == "Test Area"

    def test_init_without_salary(self):
        """Test vacancy initialization without salary data"""
        vacancy = Vacancy(
            vacancy_id="1",
            name="Test Vacancy",
            url="https://example.com",
            salary=None,
            description="Test description",
            employer="Test Employer",
            area="Test Area",
        )

        assert vacancy.salary_from == 0
        assert vacancy.salary_to == 0
        assert vacancy.salary_currency == "RUR"
        assert vacancy.salary_display == "Зарплата не указана"

    def test_salary_from_only(self):
        """Test vacancy with only 'from' salary"""
        vacancy = Vacancy(
            vacancy_id="1",
            name="Test Vacancy",
            url="https://example.com",
            salary={"from": 100000, "currency": "RUR"},
            description="Test description",
            employer="Test Employer",
            area="Test Area",
        )

        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 0
        assert vacancy.salary_display == "от 100000 RUR"

    def test_salary_to_only(self):
        """Test vacancy with only 'to' salary"""
        vacancy = Vacancy(
            vacancy_id="1",
            name="Test Vacancy",
            url="https://example.com",
            salary={"to": 150000, "currency": "RUR"},
            description="Test description",
            employer="Test Employer",
            area="Test Area",
        )

        assert vacancy.salary_from == 0
        assert vacancy.salary_to == 150000
        assert vacancy.salary_display == "до 150000 RUR"

    def test_comparison_operators(self):
        """Test vacancy comparison operators"""
        vacancy1 = Vacancy(
            vacancy_id="1",
            name="Vacancy 1",
            url="https://example.com/1",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Description 1",
            employer="Employer 1",
            area="Area 1",
        )

        vacancy2 = Vacancy(
            vacancy_id="2",
            name="Vacancy 2",
            url="https://example.com/2",
            salary={"from": 200000, "to": 250000, "currency": "RUR"},
            description="Description 2",
            employer="Employer 2",
            area="Area 2",
        )

        assert vacancy1 < vacancy2
        assert vacancy1 <= vacancy2
        assert vacancy2 > vacancy1
        assert vacancy2 >= vacancy1
        assert vacancy1 != vacancy2

        vacancy3 = Vacancy(
            vacancy_id="1",
            name="Different Name",
            url="https://example.com/3",
            salary={"from": 300000, "currency": "RUR"},
            description="Description 3",
            employer="Employer 3",
            area="Area 3",
        )

        assert vacancy1 == vacancy3

    def test_to_dict_and_from_dict(self):
        """Test conversion to dictionary and back"""
        vacancy = Vacancy(
            vacancy_id="1",
            name="Test Vacancy",
            url="https://example.com",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Test description",
            employer="Test Employer",
            area="Test Area",
        )

        vacancy_dict = vacancy.to_dict()
        new_vacancy = Vacancy.from_dict(vacancy_dict)

        assert new_vacancy.id == vacancy.id
        assert new_vacancy.name == vacancy.name
        assert new_vacancy.url == vacancy.url
        assert new_vacancy.salary_from == vacancy.salary_from
        assert new_vacancy.salary_to == vacancy.salary_to
        assert new_vacancy.description == vacancy.description
        assert new_vacancy.employer == vacancy.employer
        assert new_vacancy.area == vacancy.area

    def test_cast_to_object_list(self):
        """Test converting API response to vacancy objects"""
        vacancies_data = [
            {
                "id": "1",
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123456",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {
                    "requirement": "Python, Django, Flask",
                    "responsibility": "Backend development",
                },
                "employer": {"name": "IT Company"},
                "area": {"name": "Moscow"},
            }
        ]

        vacancies = Vacancy.cast_to_object_list(vacancies_data)

        assert len(vacancies) == 1
        assert vacancies[0].id == "1"
        assert vacancies[0].name == "Python Developer"
        assert vacancies[0].url == "https://hh.ru/vacancy/123456"
        assert vacancies[0].salary_from == 100000
        assert vacancies[0].salary_to == 150000
        assert "Python, Django, Flask" in vacancies[0].description
        assert "Backend development" in vacancies[0].description
        assert vacancies[0].employer == "IT Company"
        assert vacancies[0].area == "Moscow"
