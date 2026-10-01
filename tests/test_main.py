import pytest
from unittest.mock import patch
from main import CurrencyConverter

@pytest.fixture
def converter():
    return CurrencyConverter()

def test_convert_valid(converter):
    mock_response = {
        "rates": {
            "EUR": 0.85,
            "GBP": 0.75
        }
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        result = converter.convert(100, "USD", "EUR")
        assert result == 85.0

def test_convert_negative_amount(converter):
    with pytest.raises(ValueError, match="Amount cannot be negative."):
        converter.convert(-50, "USD", "EUR")

def test_convert_invalid_target(converter):
    mock_response = {
        "rates": {
            "EUR": 0.85
        }
    }
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        with pytest.raises(ValueError, match="Target currency 'XYZ' is not supported."):
            converter.convert(100, "USD", "XYZ")
