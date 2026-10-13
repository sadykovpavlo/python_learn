from collections import Counter, defaultdict
from collections.abc import Callable

# Повторение: списки, словари, функции, классы.
# Делаем задачи ПО ОДНОЙ — напиши решение задачи 1, я проверю, потом дам следующую.

# ЗАДАЧА 1 (функция + список словарей → словарь-счётчик)
#
# Дан список заказов (как будто response.json() от API):
orders = [
    {"id": 1, "status": "paid", "amount": 100},
    {"id": 2, "status": "pending", "amount": 50},
    {"id": 3, "status": "paid", "amount": 200},
    {"id": 4, "status": "cancelled", "amount": 30},
    {"id": 5, "status": "paid", "amount": 75},
]
#
# Напиши функцию count_by_status(orders), которая возвращает словарь
# {статус: количество заказов с этим статусом}.
#
# Например для списка выше результат должен быть:
# {"paid": 3, "pending": 1, "cancelled": 1}
#
# Пиши решение ниже этой строки:


def count_by_status(orders: list[dict[str, int | str]]) -> dict[str, int]:
    counted_status = defaultdict(int)
    for order in orders:
        counted_status[order["status"]] += 1
    return dict(counted_status)


def count_by_status_with_counter(orders: list[dict[str, int | str]]) -> dict[str, int]:
    return dict(Counter(order["status"] for order in orders))


# ЗАДАЧА 2
#
# Используя тот же список orders выше, напиши функцию
# paid_ids_by_amount_desc(orders), которая возвращает список id заказов
# со статусом "paid", отсортированный по amount ПО УБЫВАНИЮ.
#
# Для списка orders выше результат должен быть: [3, 1, 5]
# (id=3 amount=200, id=1 amount=100, id=5 amount=75)
#
# Пиши решение ниже этой строки:


# def paid_ids_by_amount_desc(orders: list[dict[str, int | str ]]) -> list[int]:
#     list_of_paid_order = [o for o in orders if o['status'] == 'paid']
#     sorted_list_with_dict = sorted(list_of_paid_order, key=lambda list_of_paid_order: list_of_paid_order['amount'], reverse=True)
#     sorted_list = [s['id'] for s in sorted_list_with_dict]
#     return sorted_list


def paid_ids_by_amount_desc(orders: list[dict[str, int | str]]) -> list[int]:
    return [
        s["id"]
        for s in sorted(
            [o for o in orders if o["status"] == "paid"],
            key=lambda o: o["amount"],
            reverse=True,
        )
    ]


# ЗАДАЧА 3
#
# Напиши класс OrderBook.
#
# - При создании принимает список заказов (такой же формат, как orders выше)
#   и сохраняет его.
# - Метод total_paid() возвращает сумму amount по всем заказам со статусом "paid".
# - Метод add_order(order) добавляет новый заказ в список. Если в переданном
#   order нет ключа "status" — метод должен бросить ValueError с текстом.
#
# Пример использования:
# book = OrderBook(orders)
# book.total_paid()  # 375  (100 + 200 + 75)
# book.add_order({"id": 6, "status": "paid", "amount": 25})
# book.total_paid()  # 400
# book.add_order({"id": 7, "amount": 10})  # -> ValueError
#
# Пиши решение ниже этой строки:


class OrderBook:
    def __init__(self, orders):
        self.orders = orders

    def total_paid(self) -> int:
        return sum(
            s["amount"] for s in [o for o in self.orders if o["status"] == "paid"]
        )

    def add_order(self, new_order: dict[str, int | str]) -> None:
        if "status" not in new_order:
            raise ValueError("Invalid value entered. oreder does not consist status")
        if "amount" not in new_order:
            raise ValueError("Invalid value entered. oreder does not consist amount")
        if "id" not in new_order:
            new_order["id"] = max([o["id"] for o in self.orders]) + 1
        self.orders.append(new_order)


# ЗАДАЧА 4
#
# Напиши класс VipOrderBook, наследующий от OrderBook.
#
# - При создании принимает orders и discount (например 0.1 означает скидку 10%).
# - Метод total_paid() должен вернуть сумму, которую вернул бы обычный
#   OrderBook.total_paid(), но уменьшенную на discount. Логику подсчёта суммы
#   не дублируй — переиспользуй то, что уже есть в родителе.
#
# Пример:
# vip_book = VipOrderBook(orders, 0.1)
# vip_book.total_paid()  # 337.5  (375 - 10%)
#
# Пиши решение ниже этой строки:


class VipOrderBook(OrderBook):
    def __init__(self, orders, discount):
        super().__init__(orders)
        self.discount = discount

    def total_paid(self):
        total = super().total_paid()
        return total - (total * self.discount)


# ЗАДАЧА 5
#
# Напиши функцию save_paid_report(orders, path), которая:
# - берёт из orders только заказы со статусом "paid"
# - записывает в файл по пути path построчно текст вида "id:amount"
#   (например строка "1:100"), одна строка на заказ
#
# Напиши вторую функцию read_report(path), которая:
# - открывает файл по пути path и возвращает список строк без символа
#   переноса строки в конце (например ["1:100", "3:200", "5:75"])
#
# Проверь сам через print, что save_paid_report(orders, "report.txt"),
# а потом read_report("report.txt") дают согласованный результат.
#
# Пиши решение ниже этой строки:


def save_paid_report(orders, path):
    paid = [p for p in orders if p["status"] == "paid"]
    with open(path, "w") as r:
        r.writelines(f"{p['id']}: {p['amount']}\n" for p in paid)


def read_report(path):
    with open(path, "r") as f:
        lines = [line.strip() for line in f]
    return lines


# print(read_report("text.txt"))

# save_paid_report(orders, 'text.txt')


# ЗАДАЧА 6
#
# Напиши декоратор log_result(func), который:
# - при каждом вызове обёрнутой функции печатает строку вида
#   "add(2, 3) -> 5" (имя функции, переданные аргументы, результат)
# - возвращает результат функции как обычно (вызывающий код не должен
#   заметить разницы, кроме того что теперь ещё печатается лог)
#
# Пример использования:
#
# @log_result
# def add(a, b):
#     return a + b
#
# add(2, 3)  # печатает "add(2, 3) -> 5", возвращает 5
#
# Пиши решение ниже этой строки:


def log_result(func: Callable):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(f"name: {func.__name__}, args: {args}, kwargs:{kwargs} result > {res}")
        return res

    return wrapper


# @log_result
# def add(a, b):
#     return a + b


# print(add(2, 5))


# ЗАДАЧА 7
#
# Напиши декоратор count_calls(func), который считает, сколько раз была
# вызвана обёрнутая функция, и при каждом вызове печатает строку вида
# "add: вызов №1", "add: вызов №2" и т.д. Функция при этом должна
# по-прежнему возвращать свой обычный результат.
#
# Пример использования:
#
# @count_calls
# def add(a, b):
#     return a + b
#
# add(2, 3)  # печатает "add: вызов №1", возвращает 5
# add(1, 1)  # печатает "add: вызов №2", возвращает 2
#
# Пиши решение ниже этой строки:


def count_calls(func: Callable):
    coll_func_count = 0

    def wraped(*args, **kwargs):
        res = func(*args, **kwargs)
        nonlocal coll_func_count
        coll_func_count += 1
        print(f"{func.__name__}: вызов №{coll_func_count}, возвращает {res}")
        return res

    return wraped


@count_calls
def add(a, b):
    return a + b


# ЗАДАЧА 8
#
# Дано:
#
products = [
    {"name": "чай", "price": 150, "in_stock": True, "category": "напитки"},
    {"name": "кофе", "price": 300, "in_stock": False, "category": "напитки"},
    {"name": "сахар", "price": 80, "in_stock": True, "category": "бакалея"},
    {"name": "мёд", "price": 500, "in_stock": True, "category": "бакалея"},
    {"name": "соль", "price": 40, "in_stock": False, "category": "бакалея"},
]


#
# Напиши функцию available_names(products), которая возвращает список имён
# (name) только тех товаров, у которых in_stock == True.
#
# available_names(products)  # ["чай", "сахар", "мёд"]
#
# Пиши решение ниже этой строки:
def available_names(products: list[dict[str, str | int | bool]]) -> list[str]:
    names = [n["name"] for n in products if n["in_stock"]]
    return names


# print(available_names(products))


# ЗАДАЧА 9
#
# Напиши функцию total_value_in_stock(products), которая возвращает сумму
# price только тех товаров, у которых in_stock == True.
#
# total_value_in_stock(products)  # 150 + 80 + 500 = 730
#
# Пиши решение ниже этой строки:


def total_value_in_stock(products: list[dict[str, str | int | bool]]) -> int | float:
    total = [p["price"] for p in products if p["in_stock"]]
    return sum(total)


# print(total_value_in_stock(products))


# ЗАДАЧА 10
#
# Напиши функцию total_value_by_category(products), которая возвращает
# словарь {category: сумма price}, только по товарам где in_stock == True.
#
# total_value_by_category(products)
# {"напитки": 150, "бакалея": 580}
#
# Пиши решение ниже этой строки:


def total_value_by_category(
    products: list[dict[str, str | int | bool]],
) -> dict[str, int | float]:
    sum_orders_by_category = defaultdict(int)
    for p in products:
        if p["in_stock"]:
            sum_orders_by_category[p["category"]] += p["price"]
    return dict(sum_orders_by_category)


# ЗАДАЧА 11
#
# Напиши функцию avg_price_by_category(products), которая возвращает словарь
# {category: средняя price}, только по товарам где in_stock == True.
#
# avg_price_by_category(products)
# {"напитки": 150.0, "бакалея": 290.0}
#
# Пиши решение ниже этой строки:


def avg_price_by_category(
    products: list[dict[str, str | int | bool]],
) -> dict[str, float]:
    count_category = defaultdict(int)
    sum_orders_by_category = defaultdict(int)
    avg_price = {}
    for p in products:
        if p["in_stock"]:
            count_category[p["category"]] += 1
            sum_orders_by_category[p["category"]] += p["price"]
    for k, v in count_category.items():
        avg_price[k] = round(sum_orders_by_category[k] / v, 2)
    return dict(avg_price)


print(avg_price_by_category(products))