from oop_drill import SafeAccount

# ═══════════════════════════════════════════════════════════════════
# НАСЛЕДОВАНИЕ. Запуск:  .venv/bin/python inheritance_drill.py
# ═══════════════════════════════════════════════════════════════════
#
# ─────────── ЗАЧЕМ ───────────
# Есть класс, который почти делает что нужно, но хочется ДОБАВИТЬ/ИЗМЕНИТЬ
# чуть-чуть, не переписывая всё заново. Наследование = "возьми готовый класс
# как основу и допили сверху". Копировать код не надо — берём и расширяем.
#
# СЛОВА:
#   Родитель (базовый класс)  — общий класс с базовой логикой.
#   Ребёнок  (подкласс)       — берёт ВСЁ от родителя + своё.
#   Синтаксис ребёнка:  class Child(Parent):   <- в скобках кого наследуем
#
# Ребёнок автоматически получает ВСЕ атрибуты и методы родителя — как будто
# они написаны в нём. Плюс может:
#   - добавить свои новые методы
#   - ПЕРЕОПРЕДЕЛИТЬ метод родителя (написать свой с тем же именем)
#
# ─────────── ЖИВОЙ ПРИМЕР (читай по строкам) ───────────

class Animal:                        # РОДИТЕЛЬ
    def __init__(self, name):
        self.name = name

    def eat(self):
        return f"{self.name} ест"

    def speak(self):
        return f"{self.name} издаёт звук"


class Dog(Animal):                   # РЕБЁНОК: Dog наследует Animal
    # НЕ пишем __init__ и eat — они УЖЕ есть от Animal, достались даром.

    def speak(self):                 # ПЕРЕОПРЕДЕЛЯЕМ: у собаки свой speak
        return f"{self.name}: гав!"

    def fetch(self):                 # НОВЫЙ метод, которого нет у Animal
        return f"{self.name} несёт мяч"


d = Dog("Рекс")                      # __init__ взялся от Animal (родителя)
print(d.eat())                       # "Рекс ест"  — метод родителя, работает даром
print(d.speak())                     # "Рекс: гав!" — переопределённый в Dog
print(d.fetch())                     # "Рекс несёт мяч" — свой метод Dog

# Вот и ответ, что значит  class ItemIn(BaseModel):
#   ItemIn наследует BaseModel из Pydantic -> получает ВСЮ его логику
#   (валидацию, парсинг json), а ты дописываешь только свои поля. Даром.


# ─────────── super(): когда ребёнку нужен __init__ родителя + своё ───────────
#
# Часто ребёнку надо: сделать ВСЁ что делал родитель в __init__, ПЛЮС своё.
# Переписывать заново — плохо. Вызываем родительский __init__ через super():

class Cat(Animal):
    def __init__(self, name, indoor):
        super().__init__(name)       # <- вызвать __init__ РОДИТЕЛЯ (он выставит self.name)
        self.indoor = indoor         # <- добавить СВОЁ поле

    def speak(self):
        return f"{self.name}: мяу"


c = Cat("Барсик", indoor=True)
print(c.name, c.indoor)              # "Барсик True" — name от родителя, indoor своё
# super().__init__(name)  = "пусть родитель сделает свою часть сборки, потом я добавлю".


# ═══════════════════════════════════════════════════════════════════
# ЗАДАЧА. Наследуемся от ТВОЕГО же SafeAccount.
#
# from oop_drill import SafeAccount   # (импортируй сверху файла)
#
# Сделай класс SavingsAccount(SafeAccount) — "накопительный счёт":
#   - в __init__ прими owner, balance И новое поле rate (процент, напр. 0.05)
#     -> вызови super().__init__(owner, balance), потом сохрани self.rate
#   - добавь НОВЫЙ метод add_interest(self):
#       начислить процент: увеличить баланс на balance * rate
#       (можешь переиспользовать свой deposit — он же достался по наследству!)
#   - методы deposit/withdraw/get_user_balance НЕ переписывай — они уже есть от родителя
#
# Проверь:
#   acc = SavingsAccount("Bob", 100, 0.05)
#   acc.deposit(50)          # метод РОДИТЕЛЯ работает -> 150
#   acc.add_interest()       # твой новый: +5% от 150 = 157.5
#   print(acc.get_user_balance())   # метод родителя тоже доступен
# ═══════════════════════════════════════════════════════════════════

class SavingsAccount(SafeAccount):
    def __init__(self, owner, balance, rate):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        self.deposit(self.balance * self.rate)




acc = SavingsAccount("bob", 50, 0.05)

acc.add_interest()
print(acc.get_user_balance())
