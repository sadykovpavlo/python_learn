import pytest
from oop_drill import SafeAccount


# ─────────────────────────────────────────────────────────────
# ОБРАЗЕЦ (готовый) — успешный deposit меняет баланс.
# ─────────────────────────────────────────────────────────────
@pytest.mark.parametrize("value, exp", [
    pytest.param(50, 150, id="int entered happy path"),
    pytest.param(1.1, 101.1, id="float entered happy path")
])
def test_deposit_increases_balance(value, exp):
    acc = SafeAccount("Bob", 100)
    acc.deposit(value)
    assert acc.balance == pytest.approx(exp)


# ═══════════════════════════════════════════════════════════════════
# ТВОИ ЗАДАЧИ. Тестируем класс, который САМ написал.
# Каждый тест: создай свежий объект -> дёрни метод -> проверь.
# ═══════════════════════════════════════════════════════════════════

# T1. withdraw успешно списывает.
#     acc = SafeAccount("Bob", 100); acc.withdraw(30); assert баланс == 70
def test_balance_degrece():
    acc = SafeAccount('Bob', 100)
    acc.withdraw(50)
    assert acc.balance == 50

# T2. deposit с невалидной суммой КИДАЕТ ValueError.
#     Вспомни pytest.raises из прошлых тестов. И используй match=... —
#     проверь, что текст ошибки именно "amount must be positive".
#     Вот тут ты на своей шкуре поймёшь, зачем в raise был нужен текст.
#     Сделай parametrize на несколько плохих сумм: 0 и отрицательную.

@pytest.mark.parametrize("value, exp", [
    pytest.param(-1, 'amount must be positive', id='minus entered exp ValueError'),
    pytest.param(0, 'amount must be positive', id='zero entered exp ValueError'),
    ])
def test_invalid_dep_value(value, exp):
    acc = SafeAccount('Bob', 50)
    with pytest.raises(ValueError, match=exp):
        acc.deposit(value)

@pytest.mark.parametrize("value, exp", [
    pytest.param('', 'amount must be int or float', id='str entered exp ValueError'),
    pytest.param([12], 'amount must be int or float', id='list[int] entered exp ValueError'),
    pytest.param({"test": 12}, 'amount must be int or float', id='dict[str: int] entered exp ValueError')
    ])
def test_invalid_dep_type(value, exp):
    acc = SafeAccount('Bob', 50)
    with pytest.raises(TypeError, match=exp):
        acc.deposit(value)



# T3. withdraw больше баланса КИДАЕТ ValueError("insufficient funds").
#     pytest.raises(ValueError, match="insufficient funds")

@pytest.mark.parametrize("value, exp", [
    pytest.param(-1, "value must mo more than 0", id="minus num, exp ValueError"),
    pytest.param(101, "insufficient funds", id="more than start balance, exp ValueError"),
    pytest.param(0, "value must mo more than 0", id="zero witdraw, exp ValueError"),
    ])
def test_invalid_value_witdraw_entered(value, exp):
    acc = SafeAccount("Bob", 100)
    with pytest.raises(ValueError, match=exp):
        acc.withdraw(value)

@pytest.mark.parametrize("value, exp", [
    pytest.param("", "amount must be int or float", id="str entered exp ValueError"),
    pytest.param([''], "amount must be int or float", id="list[str] entered exp ValueError"),
    ])
def test_invalid_type_witdraw_entered(value, exp):
    acc = SafeAccount("Bob", 100)
    with pytest.raises(TypeError, match=exp):
        acc.withdraw(value)


# T4. BOUNDARY (твоя любимая тема). Граница withdraw:
#     - снять РОВНО весь баланс (amount == balance) -> должно пройти, баланс 0
#     - снять на 1 больше баланса -> должно упасть
#     Покрой обе стороны границы.

@pytest.mark.parametrize("value, exp", [
    pytest.param(1, 99, id="Witdraw 1 exp 99"),
    pytest.param(99, 1, id="Witdraw 99 exp 1"),
    pytest.param(100, 0, id="Witdraw 100 exp 0"),
    pytest.param(99.9, 0.1, id="Witdraw 99.9 exp 0.1"),
])
def test_withdraw_boundary(value, exp):
    acc = SafeAccount('jon', 100)
    acc.withdraw(value)
    assert acc.balance == pytest.approx(exp) 




# T5. Тонкий тест-дизайн. Загляни в тело withdraw:
#         if amount <= 0 or amount > self.balance:
#             raise ValueError("insufficient funds")
#     Отрицательная сумма и "снял больше баланса" кидают ОДИН И ТОТ ЖЕ текст.
#     Вопрос: withdraw(-5) — это правда "insufficient funds"? Напиши тест, который
#     это вскрывает, и подумай — норм ли, что два разных бага дают одно сообщение.
#     (это находка тестировщика, не обязательно чинить)
