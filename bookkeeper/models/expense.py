"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: float = 0
    category: int | None = None
    expense_date: str = datetime.now().isoformat()[:19]
    added_date: str = datetime.now().isoformat()[:19]
    comment: str = ''
    pk: int = 0

    # Оформим красивый вывод для отладки
    # (разобъём его на куски в угоду pylint)
    def __str__(self) -> str:
        return f'pk = {self.pk}; amount = {self.amount}; ' \
               f'category = {self.category};\n' \
               f' exp_date = {self.expense_date}; ' \
               f'add_date = {self.added_date}; comm = {self.comment};'
    # end

    # Напишем процедуру сравнения двух элементов класса, так как иначе сравнение идёт
    # по адресу в памяти или ещё чему-то не тому
    def __eq__(self, check: Any) -> bool:
        # Проверим сначала, что совпадают типы
        if not isinstance(check, Expense):
            return NotImplemented
        else:
            FTans = ((self.pk == check.pk) and
                     (self.amount == check.amount) and
                     (self.category == check.category) and
                     (self.expense_date == check.expense_date) and
                     (self.added_date == check.added_date) and
                     (self.comment == check.comment))
            return FTans
        # end
    # end
