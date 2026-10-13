import time
from collections.abc import Callable
from functools import wraps

# Декораторы: простой декоратор, декоратор-фабрика, functools.wraps.

# ЗАДАЧА 1
#
# Напиши декоратор-фабрику retry(times).
#
# - Оборачивает функцию так: если при вызове она бросает исключение —
#   попытка повторяется, максимум times попыток всего (считая первую).
# - Если функция в итоге отработала без ошибки — вернуть её результат.
# - Если все times попыток провалились — пробросить наружу последнее
#   исключение (не глотать его молча).
# - Не забудь functools.wraps, чтобы имя функции не терялось.
#
# Пример использования (функция падает первые 2 раза, срабатывает на 3-й):
#
# attempts = {"count": 0}
#
# @retry(3)
# def flaky():
#     attempts["count"] += 1
#     if attempts["count"] < 3:
#         raise ValueError("не повезло")
#     return "success"
#
# flaky()  # вернёт "success", изнутри было 3 попытки
#
# Пиши решение ниже этой строки:


def retry(times: int):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            atempts = range(1, times + 1)
            for atempt in atempts:
                try:
                    if atempt <= times:
                        res = func(*args, **kwargs)
                    return res
                except:
                    if atempt == times:
                        raise

        return wrapper

    return decorator


attempts = {"count": 0}


@retry(3)
def flaky():
    attempts["count"] += 1
    if attempts["count"] < 3:
        raise ValueError("не повезло")
    return "success"


# print(flaky())


# ЗАДАЧА 2
#
# Напиши ПРОСТОЙ декоратор timer (без фабрики, без аргументов — просто @timer).
#
# - Замеряет, сколько времени выполнялась обёрнутая функция (time.perf_counter()
#   до и после вызова).
# - Печатает что-то вроде: "<имя функции> выполнилась за 0.1234 сек".
# - Возвращает результат функции без изменений (как будто декоратора нет).
# - Не забудь functools.wraps.
#
# Проверь сам на любой функции, например с time.sleep(0.2) внутри.


def timer(func: Callable):
    @wraps(func)
    def wrrapper(*args, **kwargs):
        time_start = time.perf_counter()
        res = func(*args, **kwargs)
        time_end = time.perf_counter()
        run_time = time_end - time_start
        print(f"{func.__name__} was running {round(run_time, 4)} sec.")
        return res

    return wrrapper


# @timer
# def sum_func(a, b):
#     time.sleep(1)
#     return a - b


def limit_calls(limit: int):
    def entered(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal limit
            if limit == 0:
                raise RuntimeError(f"{func.__name__} limet exceeded")
            res = func(*args, **kwargs)
            limit -= 1
            return res

        return wrapper

    return entered


@limit_calls(2)
def sum_func(a, b):
    if type(a) != int or type(b) != int:
        raise TypeError
    if a > 10 or b > a:
        raise ValueError
    return a - b


class Suppress:
    def __init__(self, error):
        self.error = error

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc, tb):
        return exc_type == self.error


with Suppress(ValueError):
    print(sum_func(10, 11))
