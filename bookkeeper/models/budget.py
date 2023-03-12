"""
Модель бюджета
"""
from dataclasses import dataclass
from datetime import datetime, timedelta

from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.expense import Expense


@dataclass
class Budget:
    """
    Класс бюджета. Содержит в себе:
    # time - период, за который рассчитываются траты
    # sum - потраченная сумма
    # budget - предел трат за период
    # pk - ключ
    """

    time: str = 'Empty'
    sum: float = 0
    budget: float = 0
    pk: int = 0

    def __init__(self,
                 pk: int = 0,
                 time: str = 'Empty',
                 spent_sum: float = 0,
                 budget: float = 0):
        # Проверим, что заданный период лежит в допустимом диапазоне
        if time not in ['День', 'Неделя', 'Месяц', 'Empty']:
            raise ValueError('Неизвестный тип периода!')
        # end

        self.time = time
        self.sum = spent_sum
        self.budget = budget
    # end

    # Обновление бюджета из-за изменения трат
    def update_spented_sum(self, expenses_repo: AbstractRepository[Expense]) -> None:
        """
        # Обновление бюджета из-за изменения трат
        Parameters
        ----------
        expenses_repo

        Returns
        -------

        """
        # Текущая дата в коротком формате
        date_short = datetime.now().isoformat()[:10]  # YYYY-MM-DD
        # Рассмотрим три сорта обновления: за день, за неделю, за месяц
        # За день
        if self.time == 'День':
            # Вытащим траты за день (в угоду pylint разобьём строку)
            expenses_in_time = expenses_repo.get_all(
                where={'expense_date': f'LIKE \'{date_short}%\''})
        elif self.time == 'Неделя':
            # За неделю
            # Определим текущий день недели
            weekday_now = datetime.now().weekday()
            # Определим текущую дату в удобном для работы формате
            day_now = datetime.fromisoformat(date_short)
            # Определеим дату первого дня недели
            first_week_day = day_now - timedelta(days=weekday_now)
            # Создадим лист для объектов трат
            expenses_in_time = []
            # Прогоним по всем дням недели
            for j in range(7):
                # Рассматриваемый день недели
                weekday = first_week_day + timedelta(days=j)
                # Вытащим траты за день и добавим к остальным
                # (в угоду pylint разобьём строку)
                day_expenses = expenses_repo.get_all(
                    where={'expense_date': f'LIKE \'{weekday.isoformat()[:10]}%\''})
                if day_expenses is not None:
                    expenses_in_time = expenses_in_time + day_expenses
                # end
            # end
        elif self.time == 'Месяц':
            # Вытащим траты за месяц (в угоду pylint разобьём строку)
            expenses_in_time = expenses_repo.get_all(
                where={'expense_date': f'LIKE \'{date_short[:7]}%\''})
        # end
        if (expenses_in_time == []) | (expenses_in_time is None):
            self.sum = 0
        else:
            self.sum = sum([float(expense.amount) for expense in expenses_in_time])
        # end
    # end
# end
