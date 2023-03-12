"""Всё, что отвечает за интерфейс и внешнюю логику удаления"""
from PyQt6 import QtWidgets


# Класс, описывающий строку,
# что удаляет записи расходов из таблицы
class DeleteLine(QtWidgets.QLineEdit):
    """
    # Класс, описывающий строку,
    # что удаляет записи расходов из таблицы
    """

    def __init__(self, expense_deleter=None, *args, **kwargs):
        # Всё лишнее на откуп родителю
        super().__init__(*args, **kwargs)
        # Сохраним здесь функцию удаления
        self.expense_deleter = expense_deleter

        # Вводим фоновый текст
        self.setPlaceholderText('Введи ключик расхода на удаление')
        # ВАЖНО!
        # А вот тут мы говорим, что если на клетку нажали дважды,
        # то переходим в функцию, которая будет отслеживать,
        # когда закончим редактирование
        self.textChanged.connect(self.text_is_changing)

    # end

    # Обработка события начала изменения текста - ожидаем обработки окончания ввода
    def text_is_changing(self) -> None:
        """
        # Обработка события начала изменения текста - ожидаем обработки окончания ввода
        """
        self.textChanged.disconnect(self.text_is_changing)
        print('Готовы к удалению. Ожидаем завершения ввода')
        # подключаем после окончания обработки редактирования -
        # обработку результата
        self.editingFinished.connect(self.delete_expense)

    # end

    # Обрабатывается окончание редактирования -
    # удаляем расход из таблицы расходов
    def delete_expense(self) -> None:
        """
        # Обрабатывается окончание редактирования -
        # удаляем расход из таблицы расходов
        """
        print('Ввод завершён. Начинаем удалять')
        # Отключили отслеживание редактирования
        self.editingFinished.disconnect(self.delete_expense)
        print('Отключили соединение с предыдущей командой')
        # Получили введённый текст
        pk = self.displayText()
        print(f'Получили текст. pk = {pk}')
        # Проверили, что он интовый
        print('Ключ переведён из текста в int')
        # Заранее чистим ввод
        self.clear()
        self.textChanged.connect(self.text_is_changing)

        self.expense_deleter(pk)
        print('Расход удалён')
        # end
    # end
# end
