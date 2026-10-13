"""Код под тест (SUT — system under test)."""


def top_paid(orders: list[dict], n: int) -> list[tuple[str, float]]:
    """Топ-N покупателей по сумме оплаченных заказов (по убыванию)."""
    totals: dict[str, float] = {}
    for order in orders:
        if order["status"] == "paid":
            totals[order["customer"]] = totals.get(order["customer"], 0.0) + order["amount"]
    return sorted(totals.items(), key=lambda x: x[1], reverse=True)[:n]


# orders = [
#     {"customer": "alice", "amount": 120.0, "status": "paid"},
#     {"customer": "bob",   "amount": 50.0,  "status": "paid"},
#     {"customer": "alice", "amount": 30.0,  "status": "refunded"},
#     {"customer": "carol", "amount": 200.0, "status": "paid"},
#     {"customer": "bob",   "amount": 75.0,  "status": "paid"},
# ]

# print(top_paid(orders, 3))