import pytest
from payments import convert_price


def test_get_convert_price_usd(mocker):
    mock_rate = mocker.patch("payments.get_exchange_rate", return_value = 41.5)
    currency = "USD"
    amount = 22.0
    result = convert_price(amount, currency)
    assert result == {'currency': 'USD', 'uah': 913.0, 'error': None}
    mock_rate.assert_called_once_with('USD')
    
@pytest.mark.smoke
def test_get_convert_price_usd_timeout_error(mocker):
    mock_rate = mocker.patch("payments.get_exchange_rate", side_effect = TimeoutError)
    currency = "USD"
    amount = 22.0
    result = convert_price(amount, currency)
    assert result == {'currency': 'USD', 'uah': None, 'error': 'rate_unavailable'}
    mock_rate.assert_called_once_with('USD')