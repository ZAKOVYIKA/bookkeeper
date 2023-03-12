"""
Тут описывается кусочек таблицы, отвечающей за вывод расходов и
работу пользователя с ними
"""
from PyQt6 import QtWidgets
from bookkeeper.models.expense import Expense


# Создаём класс таблицы (именно так делать не обязательно, можно и внутри исходного класса
# всё писать, а можно создать внутри класса отдельную функцию)
# Он отличается тем, что все данные о настройке таблицы мы вытащим в отдельное
# место, а потом просто воткнём в приложение.
# Также тут собрана в куску вся логика работы с данными в табличке,
# которые потом отправляются на обработку в БД и далее
class ExpenseTable(QtWidgets.QTableWidget):
    """
    #Создаём класс таблицы (именно так делать не
    обязательно, можно и внутри исходного класса
# всё писать, а можно создать внутри класса отдельную
функцию)
# Он отличается тем, что все данные о настройке
 таблицы мы вытащим в отдельное
# место, а потом просто воткнём в приложение.
# Также тут собрана в куску вся логика работы с
данными в табличке,
# которые потом отправляются на обработку в БД и далее
    """

    def __init__(self,
                 expenses_updater=None,
                 ctg_pk_2_name=None,
                 rws: int = 50,
                 clmns: int = 5,
                 header_text: str = 'Дата Сумма Категория Комментарий Ключик',
                 *args, **kwargs) -> None:
        # Всё лишнее отдаём на откуп исходнику
        super().__init__(*args, *kwargs)
        # Записываем модификатор расходов
        self.expenses_updater = expenses_updater
        # Записываем конвертер из ключа категории
        # в имя категории
        self.ctg_pk_2_name = ctg_pk_2_name

        # Задаём число столбцов
        self.setColumnCount(clmns)
        # Задаём число строк
        self.setRowCount(rws)
        # Подписываем столбцы
        self.setHorizontalHeaderLabels(header_text.split())
        # Делаем красивый вид, настраивая размеры полей.
        for j in range(clmns):
            self.resizeColumnToContents(j)
        # end
        # Заполняем таблицу пустотой, так как можем
        self.SetTableData()

        # Дополнительно для работы определим словарь, где содержится
        # конверсия названий столбцов в названия атрибутов объекта
        # затрат
        self.expenses_attrs = {0: 'expense_date',
                               1: 'amount',
                               2: 'category',
                               3: 'comment', 4
                               : 'pk'}

        # Определим, каким образом входим в редактирование таблицы.
        # В данном случае это двойной щелчок мыши
        # (и, вообще, такой вход стоит по умолчанию)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked)

        # ВАЖНО!
        # А вот тут мы говорим, что если на клетку нажали дважды,
        # то переходим в функцию, которая будет отслеживать,
        # когда закончим редактирование
        self.cellDoubleClicked.connect(self.cell_double_clicked)

    # end

    # Дополнительно введём функцию для ввода данных
    # Функция заполнения полей таблицы
    def SetTableData(self, data: list[list[str]] = None) -> None:
        """
         # Функция заполнения полей таблицы
        Parameters
        ----------
        data

        Returns
        -------

        """
        if data is None:
            data = [['empty' for j in range(self.columnCount())]
                    for j in range(self.rowCount())]
        # end

        # Сохраним данные в нашем объекте
        self.data = data

        # Вносим данные
        for j, row in enumerate(data):
            for k, x in enumerate(row):
                self.setItem(j, k, QtWidgets.QTableWidgetItem(x))
            # end
        # end
        # Делаем красивый вид, настраивая размеры полей.
        for j in range(self.columnCount()):
            self.resizeColumnToContents(j)
        # end

    # end

    # Обработка события двойного щелчка - ожидаем обработки редактирования
    def cell_double_clicked(self, row: int, columns: int) -> None:
        """# Обработка события двойного щелчка - ожидаем обработки редактирования"""
        print('Начали ожидать конца редактирования')
        # КАК ПЕРЕДАЁМ СТРОКУ И СТОЛБЕЦ????
        # подключаем после окончания обработки редактирования -
        # обработку результата
        self.cellChanged.connect(self.cell_changed)

    # end

    # Обрабатывается окончание редактирования -
    # составляем новые параметры записи
    def cell_changed(self, row, column) -> None:
        """    # Обрабатывается окончание редактирования -
    # составляем новые параметры записи"""
        print('Приступили к обработке события после конца редактирования')
        # Отключили отслеживание редактирования
        self.cellChanged.disconnect(self.cell_changed)
        print('Отключили кнопку, чтобы не было дублирования')
        # Определили запись с каким ключом редактировали.
        pk = self.data[row][-1]
        print('Определили ключ записи')
        # Новые параметры затраты
        new_val = self.item(row, column).text()
        print('Определили новые параметры затраты')
        # По словарю вернём имя атрибута объекта, к которому
        # присвоим новое значение
        attr = self.expenses_attrs[column]
        print('Вернули имя атрибута, которому меняли значение')
        # Отправим новые данные в функцию exp_updater,
        # которая определена в View.
        # Во View она принимает их bookkeeper модификатор
        # записи в БД и возвращающий значения для таблицы.
        # Т.е. это вход в прокладку между View и Repository
        print('Передаём данные в обработчик обновлений затрат')
        self.expenses_updater(pk, [attr], [new_val])

    # end

    # Запись в таблицу расходов из БД
    def set_expenses(self, expenses: list[Expense]) -> None:
        """
        # Запись в таблицу расходов из БД
        Parameters
        ----------
        expenses

        Returns
        -------

        """
        # Сохраним в нашем классе расходы
        self.expenses = expenses
        # Переведём данные из формата Expenses в строки
        self.data = self.expenses_to_data(self.expenses)
        # Очистим содержимое таблицы
        self.clearContents()
        # Занесём данные в таблицу
        self.SetTableData(self.data)

    # end

    # Конвертер из типов характерных для Expenses
    # в строки
    def expenses_to_data(self, expenses: list[Expense] | None) -> list[list[str]]:
        """
            # Конвертер из типов характерных для Expenses
    # в строки
        Parameters
        ----------
        expenses

        Returns
        -------

        """
        # Создадим заранее лист для ответов
        data = []
        # Проверим, что записи вообще есть:
        if expenses is None:
            data = [['Empty', 'Empty', 'Empty', 'Empty', 'Empty']]
        else:
            # Прогоним каждый расход
            for expense in expenses:
                # Разложим трату на лист из строк
                item = [str(expense.expense_date),
                        str(expense.amount),
                        str(self.ctg_pk_2_name(expense.category)),
                        str(expense.comment),
                        str(expense.pk)]
                # Присоединим этот лист к остальным
                data.append(item)
            # end
        # end
        # Вернём ответ
        return data
    # end
# end
