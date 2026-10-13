# Контекстные менеджеры: свой класс с __enter__/__exit__.
# Разбито на 3 маленьких шага — делаем по одному, без забегания вперёд.

from review_drill import OrderBook
from contextlib import contextmanager

# ШАГ A
#
# Напиши класс PrintingGuard. Никакой бизнес-логики, только механика.
#
# - __enter__ печатает "вход" и возвращает что угодно (хоть self).
# - __exit__ печатает "выход" и возвращает False.
#
# Проверь сам: создай PrintingGuard и используй его в with-блоке с любым
# простым кодом внутри (например print("привет")). Убедись, что видишь
# порядок: "вход" -> твой код -> "выход".


class PrintingGuard:
    def __enter__(self):
        print("entered")

    def __exit__(self, exc_type, exc, tb):
        print("exit")


# with PrintingGuard():
#     print("привет")


# ШАГ B
#
# Скопируй PrintingGuard в новый класс PrintingGuardWithCheck (или измени
# этот же) и добавь в __exit__ проверку: если была ошибка внутри блока
# (exc_type не None) — напечатай "была ошибка: <текст ошибки>", иначе —
# напечатай "ошибок не было". __exit__ всё ещё возвращает False (ошибку
# не глушим).
#
# Проверь сам ДВАЖДЫ: один раз с обычным кодом внутри блока (без ошибок),
# второй раз — с raise ValueError("test") внутри блока (оберни вызывающий
# код в try/except снаружи, иначе программа упадёт — это нормально, мы же
# не глушим исключение).


class PrintingGuardWithCheck:
    def __enter__(self):
        print("enttred here")

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            print(f"Error occured {exc_type}")
        else:
            print("all good")
        return False


# with PrintingGuardWithCheck():
#     raise ValueError('some message')


# ШАГ C (финал — собираем всё вместе)
#
# Напиши класс OrderBookTransaction — контекстный менеджер-"транзакция" для OrderBook.
#
# - При создании принимает объект OrderBook.
# - При входе в блок with сохрани копию текущего списка book.orders (бэкап),
#   и верни САМ book (не бэкап!) — внутри блока нужно работать с настоящим book.
# - Если блок with отработал БЕЗ ошибок — ничего откатывать не нужно,
#   изменения, сделанные внутри блока, остаются как есть.
# - Если внутри блока with вылетело исключение — list book.orders должен
#   откатиться к состоянию ДО входа в блок (как будто изменений не было),
#   а само исключение должно полететь дальше наружу (не глотай его).
#
# Пример использования:
#
# book = OrderBook(orders.copy())
# starting_len = len(book.orders)
#
# try:
#     with OrderBookTransaction(book):
#         book.add_order({"id": 20, "status": "paid", "amount": 999})
#         raise RuntimeError("что-то пошло не так")
# except RuntimeError:
#     pass
#
# print(len(book.orders) == starting_len)  # True — откат сработал


class OrderBookTransaction:
    def __init__(self, book):
        self.book = book

    def __enter__(self):
        self.back_up = self.book.orders.copy()
        return self.book

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.book.orders[:] = self.back_up
            return False
        else:
            pass
        return False


orders_list = []
book = OrderBook(orders_list)

try:
    with OrderBookTransaction(book):
        book.add_order({'id': 1, 'amount': 100})
except ValueError as e:
    print(f'Error {e}')



@contextmanager
def print_guard():
    print("enter")
    try: 
        yield
    except Exception as ex:
        print(f"Error occured {ex}")
        raise
    finally:
        print("exit")



with print_guard():
    raise ValueError("TEST")


# ШАГ E (contextlib.contextmanager)
#
# Перепиши PrintingGuard (из Шага A), но теперь НЕ классом, а функцией-генератором
# с декоратором @contextmanager:
#
# - до yield — печатает "вход"
# - после yield — печатает "выход"
#
# Проверь сам в with-блоке с любым простым кодом внутри — должен увидеть тот же
# порядок, что и в Шаге A: "вход" -> твой код -> "выход".

