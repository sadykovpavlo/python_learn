# ═══════════════════════════════════════════════════════════════════
# ООП С НУЛЯ. Запуск:  .venv/bin/python oop_drill.py
# ═══════════════════════════════════════════════════════════════════
#
# ─────────── ЗАЧЕМ ЭТО ВООБЩЕ НУЖНО ───────────
#
# Представь: ты описываешь СОБАКУ. У собаки есть ДАННЫЕ (кличка, возраст)
# и ДЕЙСТВИЯ (лаять, есть). Пока собака одна — можно хранить в переменных:
#     dog_name = "Рекс"
#     dog_age = 3
# Но собак много. Заводить dog1_name, dog2_name, dog3_name... — ад.
# А ещё действие "лаять" должно знать, ЧЬЯ кличка, чтобы напечатать "Рекс: гав".
# Данные расползаются, функции отдельно, связь теряется.
#
# ООП решает это так: СКЛЕИВАЕМ данные и действия в один "предмет".
#
# ─────────── ДВА СЛОВА, КОТОРЫЕ НАДО РАЗЛИЧАТЬ ───────────
#
# КЛАСС  — это ЧЕРТЁЖ / шаблон. Описание "что такое собака вообще".
#          Сам по себе класс — не собака, это бланк. Собак из него ещё нет.
#
# ОБЪЕКТ — это конкретная собака, СОЗДАННАЯ по чертежу. Рекс. Или Бобик.
#          Один класс -> сколько угодно объектов, каждый со СВОИМИ данными.
#          (класс "Собака" один, а Рекс и Бобик — два разных объекта)
#
# Аналогия: класс = форма для печенья. Объекты = сами печеньки.
# Форма одна, печенек много, и каждую можно посыпать по-своему.
#
# ─────────── РАЗБОР ЖИВОГО ПРИМЕРА (читай по строкам) ───────────

class Dog:                          # объявляем ЧЕРТЁЖ по имени Dog

    def __init__(self, name, age):  # __init__ — "сборка": что делать при создании собаки
        # self — это "ВОТ ЭТА конкретная собака, которую сейчас создаём".
        # self.name — прикрепить кличку К ЭТОЙ собаке (её собственная ячейка данных)
        self.name = name
        self.age = age

    def bark(self):                 # действие. self = та собака, у которой вызвали bark
        # благодаря self метод ЗНАЕТ, чья это кличка:
        return f"{self.name}: гав!"


# (демо создания объектов Dog и SafeAccount — внизу файла, под if __name__ == "__main__")

# ─────────── ПОЧЕМУ self ─────────────────────────────────────────
# Смотри фокус: bark ОБЪЯВЛЕН с параметром self  ->  def bark(self)
#               а ВЫЗЫВАЕШЬ без аргументов        ->  rex.bark()
# Когда пишешь  rex.bark(), Python сам подставляет rex на место self.
# То есть rex.bark()  превращается внутри в  bark(rex).
# self — это способ метода узнать "на каком именно объекте меня вызвали".
# Без self метод не знал бы, ЧЬЮ кличку печатать — Рекса или Бобика.
# ══════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════
# ЗАДАЧА 1 (пиши ниже). Класс BankAccount ("банковский счёт").
#   При создании счёта задаём владельца и стартовый баланс.
#   __init__(self, owner, balance)  -> сохрани оба в self
#   deposit(self, amount)           -> увеличь баланс на amount, верни новый баланс
#   withdraw(self, amount)          -> уменьши баланс на amount, верни новый баланс
#
#   Потом создай ДВА разных счёта и подёргай — убедись, что балансы независимы:
#     acc = BankAccount("Bob", 100)
#     print(acc.deposit(50))    # 150
#     print(acc.withdraw(30))   # 120
# ═══════════════════════════════════════════════════════════════════


class BankAccount:
    def __init__(self, owner: str, balance: int):
        self.owner = owner
        self.balance = balance

    def deposit(self, incoming_balance: int) -> None:
        self.balance += incoming_balance

    def withdraw(self, out_balance: int) -> None:
        self.balance -= out_balance

    def get_user_balance(self) -> str:
        return f"{self.owner} has {self.balance} on balance"
        

# ═══════════════════════════════════════════════════════════════════
# ЗАДАЧА 2. Защита данных — вот ЗАЧЕМ класс, а не просто dict.
#
# Сделай НОВЫЙ класс SafeAccount (скопируй свой BankAccount и допили):
#
#   1. withdraw(self, amount):
#        - если amount БОЛЬШЕ текущего баланса -> raise ValueError("insufficient funds")
#          (нельзя уйти в минус — счёт САМ себя защищает)
#        - иначе списать как обычно
#
#   2. deposit(self, amount):
#        - если amount <= 0 -> raise ValueError("amount must be positive")
#          (нельзя положить ноль или минус)
#        - иначе зачислить
#
# Идея: объект не просто хранит balance — он СТЕРЕЖЁТ свои правила.
# dict такого не умеет: d["balance"] -= 999 молча уведёт в минус, никто не остановит.
# А метод withdraw может проверить и не пустить. В этом сила класса.
#
# Проверь оба сценария сам:
#   acc = SafeAccount("Bob", 100)
#   acc.withdraw(30)     # ок, 70
#   acc.withdraw(999)    # должно упасть ValueError
#
# Падение поймай через try/except, чтобы скрипт не рухнул на первом же raise:
#   try:
#       acc.withdraw(999)
#   except ValueError as e:
#       print("поймали ошибку:", e)
# ═══════════════════════════════════════════════════════════════════

class SafeAccount:
    def __init__(self, owner: str, balance: int):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: int) -> None:
        if not isinstance(amount, (int, float)):
            raise TypeError("amount must be int or float")
        if amount <= 0:
            raise ValueError ("amount must be positive")
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        if not isinstance(amount, (int, float)):
            raise TypeError("amount must be int or float")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        if amount <= 0:
            raise ValueError("value must mo more than 0")
        self.balance -= amount

    def get_user_balance(self) -> str:
        return f"{self.owner} has {self.balance} on balance"


