"""Фейковый ресурс для тренировки фикстур с teardown.
Не настоящая БД — просто объект, у которого видно состояние (open/closed)
и который копит строки. На нём удобно прочувствовать setup -> тест -> teardown."""


class FakeDB:
    def __init__(self) -> None:
        self.is_open: bool = False
        self.rows: list[dict] = []

    def connect(self) -> None:
        """SETUP-часть: 'открыть соединение'."""
        self.is_open = True
        print("  [FakeDB] connect() — соединение открыто")

    def close(self) -> None:
        """TEARDOWN-часть: 'закрыть соединение'."""
        self.is_open = False
        print("  [FakeDB] close() — соединение закрыто")

    def insert(self, row: dict) -> None:
        if not self.is_open:
            raise RuntimeError("Нельзя писать в закрытое соединение!")
        self.rows.append(row)
