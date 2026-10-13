"""Код под тест с ВНЕШНИМ вызовом (send_email), который в тестах мокаем."""

from orders import top_paid


def send_email(to: str, subject: str) -> None:
    """'Внешний' сервис. В реальности слал бы настоящее письмо по сети.
    В тестах мы его мокаем, чтобы ничего реально не отправлять."""
    # представь тут настоящую отправку через SMTP / API
    raise RuntimeError("Настоящая отправка письма! В тесте так быть не должно.")


def notify_top_customer(orders: list[dict]) -> str | None:
    """Находит топ-1 покупателя и шлёт ему письмо. Возвращает имя или None."""
    top = top_paid(orders, 1)
    if not top:
        return None
    name = top[0][0]
    send_email(name, "Вы наш лучший покупатель!")
    return name
