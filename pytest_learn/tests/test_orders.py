import pytest
from orders import top_paid

@pytest.fixture
def orders():
     orders = [
            {"customer": "alice", "amount": 120.0, "status": "paid"},
            {"customer": "bob",   "amount": 50.0,  "status": "paid"},
            {"customer": "alice", "amount": 30.0,  "status": "refunded"},
            {"customer": "carol", "amount": 200.0, "status": "paid"},
            {"customer": "bob",   "amount": 75.0,  "status": "paid"},
        ]
     return orders

@pytest.mark.smoke
def test_top_paid_return_top_2_by_amount(orders):
    result = top_paid(orders, 2)
    assert result == [('carol', 200.0), ('bob', 125.0)] 

@pytest.mark.parametrize("n, expected", [
    (1, [('carol', 200.0)]),
    (2, [('carol', 200.0), ('bob', 125.0)]),
    (3, [('carol', 200.0), ('bob', 125.0), ('alice', 120.0)])
])
def test_top_paid_return_castom_n_by_amount(orders, n, expected):
    result = top_paid(orders, n)
    assert result == expected