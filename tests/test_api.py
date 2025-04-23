from unittest.mock import MagicMock, patch

import pytest

from src.api import HH


class TestHH:
    @patch("src.api.requests.get")
    def test_connect_success(self, mock_get):
        """Test successful API connection"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        file_worker = MagicMock()
        hh = HH(file_worker)

        hh._connect()

        mock_get.assert_called_once()

    @patch("src.api.requests.get")
    def test_connect_failure(self, mock_get):
        """Test failed API connection"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        file_worker = MagicMock()
        hh = HH(file_worker)

        with pytest.raises(ConnectionError):
            hh._connect()

    @patch("src.api.requests.get")
    def test_get_vacancies(self, mock_get):
        """Test getting vacancies from API"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": "1", "name": "Test Vacancy"}],
            "pages": 1,
        }
        mock_get.return_value = mock_response

        file_worker = MagicMock()
        hh = HH(file_worker)

        result = hh.get_vacancies("python")

        assert len(result) == 1
        assert result[0]["id"] == "1"
        assert result[0]["name"] == "Test Vacancy"

        mock_get.assert_called()
