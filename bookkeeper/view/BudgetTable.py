"""
Тут описывается кусочек таблицы, отвечающей за вывод бюджета и
работу пользователя с ним
"""
from typing import Any
from PyQt6 import QtWidgets
from bookkeeper.models.budget import Budget


class BudgetTable(QtWidgets.QTableWidget):
    """
    #Создаём класс таблицы (именно так делать не обязательно,
    можно и внутри исходного класса
    # всё писать, а можно создать внутри класса отдельную функцию)
    # Он отличается тем, что все данные о настройке
    таблицы мы вытащим в отдельное
    # место, а потом просто воткнём в приложение.
    # Также тут собрана в кучку вся логика работы с данными в табличке,
    # которые потом отправляются на обработку в БД и далее
    """

    def __init__(self,
                 budget_modifier=None,
                 rws: int = 3,
                 clmns: int = 4,
                 header_text: str = 'Срок Сумма Бюджет Ключик',
                 *args, **kwargs) -> None:
        # Всё лишнее отдаём на откуп исходнику
        super().__init__(*args, *kwargs)
        # Задаём функцию обновления бюджета
        self.budget_modifier = budget_modifier
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
        self.SetTableData([['День', 'empty', 'empty'],
                           ['Неделя', 'empty', 'empty'],
                           ['Месяц', 'empty', 'empty']])

        # Дополнительно для работы определим словарь, где содержится
        # конверсия названий столбцов в названия атрибутов объекта
        # затрат
        self.budget_attrs = {0: 'День', 1: 'Неделя', 2: 'Месяц'}

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
    def SetTableData(self, data: list[list[Any]] | None = None) -> None:
        """
        # Функция заполнения полей таблицы
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
        """
        # Обработка события двойного щелчка - ожидаем обработки редактирования
        """
        print('Начали ожидать конца редактирования')
        # подключаем после окончания обработки редактирования -
        # обработку результата
        self.cellChanged.connect(self.cell_changed)
    # end

    # Обрабатывается окончание редактирования -
    # составляем новые параметры записи
    def cell_changed(self, row, column) -> None:
        """
        # Обрабатывается окончание редактирования -
        # составляем новые параметры записи
        """
        print('Приступили к обработке события после конца редактирования')
        # Отключили отслеживание редактирования
        self.cellChanged.disconnect(self.cell_changed)
        # Определили запись с каким ключом редактировали.
        pk = self.data[row][-1]
        print('Определили ключ записи')
        # Новые параметры бюджета
        new_val = self.item(row, column).text()
        print('Определили новые параметры бюджета')
        # По словарю вернём имя атрибута объекта, к которому
        # присвоим новое значение
        attr = self.budget_attrs[row]
        print('Вернули имя атрибута, которому меняли значение')
        # Отправим новые данные в функцию exp_updater,
        # которая определена в View.
        # Во View она принимает их bookkeeper модификатор
        # записи в БД и возвращающий значения для таблицы.
        # Т.е. это вход в прокладку между View и Repository
        print(f'Передаём на вход: {pk}, {new_val}, {attr}')
        self.budget_modifier(pk, new_val, attr)

    # end

    # Запись в таблицу бюджета из БД
    def set_budgets(self, budgets: list[Budget]) -> None:
        """ # Запись в таблицу бюджета из БД """
        # Сохраним в нашем классе расходы
        self.budgets = budgets
        # Переведём данные из формата Budget в строки
        self.data = self.budgets_to_data(self.budgets)
        # Очистим содержимое таблицы
        self.clearContents()
        # Занесём данные в таблицу
        self.SetTableData(self.data)

    # end

    # Конвертер из типов характерных для Budget
    # в строки
    def budgets_to_data(self, budgets: list[Budget]) -> list[list[str]]:
        """
        # Конвертер из типов характерных для Budget
        # в строки
        Parameters
        ----------
        budgets

        Returns
        -------

        """
        # Создадим заранее лист для ответов
        data = []
        # Проверим, что существуют хоть какие-то бюджеты:
        if budgets is None:
            data = [['День', '', 'Не определён', ''],
                    ['Неделя', '', 'Не определён', ''],
                    ['Месяц', '', 'Не определён', '']]
        else:
            # Прогоним каждый расход
            for time in ['День', 'Неделя', 'Месяц']:
                # Ищем бюджеты, соответствующие периоду time
                budget = [bdg for bdg in budgets if bdg.time == time]
                # Если таковых не найдено, то бюджет на таокй срок не установлен
                if len(budget) == 0:
                    # Добавляем к данным
                    data.append([time, '', 'Не определён', ''])
                else:
                    bdg = budget[0]
                    # Разложим трату на лист из строк
                    data.append([str(bdg.time),
                                 str(bdg.sum),
                                 str(bdg.budget),
                                 str(bdg.pk)])
                # end
            # end
        # end
        # Вернём ответ
        return data
    # end
# end
