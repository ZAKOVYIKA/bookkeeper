""" Полное описание основного рабочего окна"""
import os
from PyQt6 import QtWidgets, QtGui
from bookkeeper.view.ExpensesTable import ExpenseTable
from bookkeeper.view.BudgetTable import BudgetTable
from bookkeeper.view.DeleteLine import DeleteLine
from bookkeeper.view.ExpAddCompany import ExpAddCompany
from bookkeeper.models.category import Category

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Start_pic_path = os.path.join(BASE_DIR, 'StartPic.jpg')


# Создаём класс окна, в котором опишем основную начинку
class BookkeeperWindow(QtWidgets.QWidget):
    """ Класс основного рабочего окна"""

    def __init__(self,
                 ctg: list[Category] = [Category('Empty')],
                 expenses_adder=None,
                 expenses_updater=None,
                 expenses_deleter=None,
                 ctg_pk_2_name=None,
                 category_adder=None,
                 category_updater=None,
                 category_deleter=None,
                 budget_updater=None,
                 *args, **kwargs):
        # Так как переопределяем init, то сначала
        # надо передать все системные аргументы туда, где они нужны,
        # а потом уже городить свой код
        super().__init__(*args, **kwargs)

        # Опишем элементы окна сверху вниз, слева-направо

        # Подпись у таблички
        self.TableLabel = self.MakeLabel('Таблица последних расходов')

        # Поле для удаления расхода
        self.DeleteLine = DeleteLine(expenses_deleter)
        self.DeleteLine.setMaximumWidth(300)
        # Таблица расходов
        # Вариант с созданием отдельного класса таблицы
        self.ExpensesTable = ExpenseTable(expenses_updater, ctg_pk_2_name)

        # Подпись к таблице с бюджетом
        self.BudgetLabel = self.MakeLabel('Бюджет')

        # Таблица бюджета
        self.BudgetTable = BudgetTable(budget_updater)

        # Кусок с вводом данных расхода и редактурой категории
        self.ExpenseAndCategoryEdit = ExpAddCompany(ctg,
                                                    expenses_adder,
                                                    category_adder,
                                                    category_updater,
                                                    category_deleter)

        # Строим красивую раскладку (можно было бы и в отдельную функцию
        # загнать, но мне лень выяснять типы)

        # Имя таблицы и поле для удаления соберём вместе
        horiz0 = QtWidgets.QHBoxLayout()
        # Подпись таблицы
        horiz0.addWidget(self.TableLabel)
        # Строка для удаления расходов
        horiz0.addWidget(self.DeleteLine)

        # Разложим сюда то, что раскладывается просто сверху вниз
        vert1 = QtWidgets.QVBoxLayout()
        # Нулевой горизонтальный блок, что описан выше
        vert1.addLayout(horiz0)
        # Таблицу расходов
        vert1.addWidget(self.ExpensesTable)
        # Подпись бюджета
        vert1.addWidget(self.BudgetLabel)
        # Таблицу бюджета
        vert1.addWidget(self.BudgetTable)
        # Кусок изменения всего
        vert1.addWidget(self.ExpenseAndCategoryEdit)

        # Дополнительно создадим поле для картиночки
        self.PicField1 = QtWidgets.QLabel()
        self.pixmap1 = QtGui.QPixmap('StartPic.jpg')
        print(self.pixmap1.isNull())
        self.PicField1.setPixmap(self.pixmap1)
        self.PicField1.setScaledContents(True)
        self.PicField1.setMaximumWidth(300)
        self.PicField1.setMaximumHeight(300)

        # и личной подписи
        self.SignField = QtWidgets.QLabel('Выполнил: Нежин А.Н. М02-202кф')

        # Дополнительно создадим поле для картиночки
        self.PicField2 = QtWidgets.QLabel()
        self.pixmap2 = QtGui.QPixmap('LastPic.jpg')
        print(self.pixmap2.isNull())
        self.PicField2.setPixmap(self.pixmap2)
        self.PicField2.setScaledContents(True)
        self.PicField2.setMaximumWidth(250)
        self.PicField2.setMaximumHeight(300)

        #Добьём раскладку
        ver = QtWidgets.QVBoxLayout()
        ver.addWidget(self.PicField1)
        ver.addWidget(self.SignField)

        hor = QtWidgets.QHBoxLayout()
        hor.addLayout(ver)
        hor.addLayout(vert1)
        hor.addWidget(self.PicField2)

        # Присвоим полученную раскладку соотв. полю self
        self.layout = hor
        # Применим эту раскладку к окну
        self.setLayout(self.layout)

    # end

    # Функция создания подписи у чего-либо
    def MakeLabel(self, text: str = 'empty label') -> QtWidgets.QLabel:
        """# Функция создания подписи у чего-либо"""
        # Создаём подпись
        label_obj = QtWidgets.QLabel()
        # Присваиваем ей имя
        label_obj.setText(text)
        # Возвращаем её
        return label_obj

    # end

    # Функция создания поля с возможностью ввода
    def MakeLineEdit(self, text: str = '') -> QtWidgets.QLineEdit:
        """# Функция создания поля с возможностью ввода"""

        # Создаём строку объект строки ввода
        LineEdit_obj = QtWidgets.QLineEdit()
        # Делаем фоновую подпись
        LineEdit_obj.setPlaceholderText(text)
        # Возвращаем его
        return LineEdit_obj

    # end

    # Функция создания кнопки
    def MakeButton(self, text: str = 'empty button') -> QtWidgets.QPushButton:
        """ # Функция создания кнопки"""
        # Создали объект кнопки
        Button_obj = QtWidgets.QPushButton(text)
        # Вернули его
        return Button_obj
    # end
# end
