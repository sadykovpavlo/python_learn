import pytest
from notifier import notify_top_customer


@pytest.fixture
def orders():
    orders = [
        {"customer": "alice", "amount": 120.0, "status": "paid"},
        {"customer": "carol", "amount": 200.0, "status": "paid"},
    ]
    return orders


def test_top_1_customer_nitifier(orders, mocker):
    mock_send = mocker.patch("notifier.send_email")
    result = notify_top_customer(orders)
    assert result == "carol"
    mock_send.assert_called_once_with("carol", "Вы наш лучший покупатель!")
