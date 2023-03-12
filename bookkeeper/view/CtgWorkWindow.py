"""Всё, что касается окна редактирования категорий и его функционала"""
from PyQt6 import QtWidgets, QtGui


# Создадим окно редактирования категории
class CategoryAUDWindow(QtWidgets.QWidget):
    """# Создадим окно редактирования категории"""

    def __init__(self,
                 ctg_adder=None,
                 ctg_updater=None,
                 ctg_deleter=None,
                 *args, **kwargs):
        # Спихнём всё лишнее на родителя
        super().__init__(*args, **kwargs)
        print('Выполнен вход в окно редактирования категорий')
        # Сохраним функции добавления, обновления и удаления в классе
        self.ctg_adder = ctg_adder
        self.ctg_updater = ctg_updater
        self.ctg_deleter = ctg_deleter

        # Создадим подпись
        self.ButtonLabel = self.MakeLabel('Выбери один из вариантов')

        # Создадим три кнопки
        # Создания
        self.CtgAddCheck = self.MakeButton('Создать категорию')
        # Обновления
        self.CtgUpdCheck = self.MakeButton('Обновить категорию')
        # Удаления
        self.CtgDelCheck = self.MakeButton('Удалить категорию')

        # Создадидм три поля
        # Имя категории
        self.CtgName = self.MakeLineEdit(
            'Введи имя категории БЕЗ ПРОБЕЛОВ. Чувствителен к регистру.')
        # Родитель категории
        self.CtgParent = self.MakeLineEdit(
            'Введи имя родителя БЕЗ ПРОБЕЛОВ. Чувствителен к регистру.')
        # Дети
        self.CtgChildrens = self.MakeLineEdit(
            'Введи имена детей через пробелы. (На свой страх и риск)')

        # Создадим кнопку подтверждения
        self.AcceptButton = self.MakeButton('Подтвердить')

        # Соберём картинку
        # Дополнительно создадим поле для картиночки
        self.PicField = QtWidgets.QLabel()
        self.pixmap = QtGui.QPixmap('AnothPic.jpg')
        print(self.pixmap.isNull())
        self.PicField.setPixmap(self.pixmap)
        self.PicField.setScaledContents(True)
        self.PicField.setMaximumWidth(450)
        self.PicField.setMaximumHeight(500)

        # Соберём в красивую кучку

        # Создадим вертикальную раскладку
        vert = QtWidgets.QVBoxLayout()
        # Добавим картинку
        vert.addWidget(self.PicField)
        # Добавим в неё подпись
        vert.addWidget(self.ButtonLabel)

        # Заполним ряд кнопок
        horiz = QtWidgets.QHBoxLayout()
        # Кнопочки
        horiz.addWidget(self.CtgAddCheck)
        horiz.addWidget(self.CtgUpdCheck)
        horiz.addWidget(self.CtgDelCheck)

        # Вкинем в вертикальную
        vert.addLayout(horiz)

        # Добавим поля ввода
        vert.addWidget(self.CtgName)
        vert.addWidget(self.CtgParent)
        vert.addWidget(self.CtgChildrens)

        # Добавим кнопку подтверждения
        vert.addWidget(self.AcceptButton)

        # Примем эту раскладку
        self.setLayout(vert)

        # Заблокируем кнопочки, чтобы никто не заполнял лишнего
        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        # Привяжем верхние кнопки к действиям
        self.CtgAddCheck.clicked.connect(self.ctg_add1)
        self.CtgUpdCheck.clicked.connect(self.ctg_upd1)
        self.CtgDelCheck.clicked.connect(self.ctg_del1)

        print('Окно сформировано')
    # end

    # Добавление часть 1
    def ctg_add1(self) -> None:
        """# Добавление часть 1"""
        print('Вошли в режим добавления')

        # Заблокируем остальные кнопки и разблокируем заблокированные
        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_add2)
    # end

    # Добавление часть 2
    def ctg_add2(self) -> None:
        """# Добавление часть 2"""
        # ОБЯЗАТЕЛЬНО ОТКЛЮЧИМ КНОПКУ иначе будут дублироваться команды!!
        self.AcceptButton.clicked.disconnect(self.ctg_add2)
        print('Начат второй этап добавления')
        # Выполним добавление
        print(f'{self.CtgName.text()}, '
              f'{self.CtgParent.text()}, '
              f'{self.CtgChildrens.text()}')
        self.ctg_adder(self.CtgName.text(),
                       self.CtgParent.text(),
                       self.CtgChildrens.text())
        print('Добавление в БД выполнено')
        # Очистим поля
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        # Вернём кнопки в исходное состояние
        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Добавление завершено. Сброс до исходного состояния произведён.')
    # end

    # обновление часть 1
    def ctg_upd1(self) -> None:
        """# обновление часть 1"""
        print('Вошли в режим обновления')
        # Заблокируем остальные кнопки и разблокируем заблокированные
        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_upd2)
    # end

    # обновление часть 2
    def ctg_upd2(self) -> None:
        """# обновление часть 2"""
        # ОБЯЗАТЕЛЬНО ОТКЛЮЧИМ КНОПКУ
        # иначе будут дублироваться команды!!
        self.AcceptButton.clicked.disconnect(self.ctg_upd2)
        print('Начат второй этап обновления')
        # Выполним добавление
        print(f'{self.CtgName.text()}, '
              f'{self.CtgParent.text()}, '
              f'{self.CtgChildrens.text()}')
        self.ctg_updater(self.CtgName.text(),
                         self.CtgParent.text(),
                         self.CtgChildrens.text())
        print('Обновление в БД выполнено')
        # Очистим поля
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        # Вернём кнопки в исходное состояние
        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Обновление завершено. Сброс до исходного состояния произведён.')
    # end

    # Удаление часть 1
    def ctg_del1(self) -> None:
        """# Удаление часть 1"""
        print('Вошли в режим удаления')
        # Заблокируем остальные кнопки и разблокируем заблокированные
        self.CtgName.setDisabled(False)
        self.CtgParent.setDisabled(False)
        self.CtgChildrens.setDisabled(False)
        self.AcceptButton.setDisabled(False)

        self.CtgAddCheck.setDisabled(True)
        self.CtgUpdCheck.setDisabled(True)
        self.CtgDelCheck.setDisabled(True)

        print('Кнопки заблокированы')

        self.AcceptButton.clicked.connect(self.ctg_del2)
    # end

    # Удаление часть 2
    def ctg_del2(self) -> None:
        """# Удаление часть 2"""
        # ОБЯЗАТЕЛЬНО ОТКЛЮЧИМ КНОПКУ иначе будут дублироваться команды!!
        self.AcceptButton.clicked.disconnect(self.ctg_del2)
        print('Начат второй этап удаления')
        # Выполним удаление
        print(f'{self.CtgName.text()}')
        self.ctg_deleter(self.CtgName.text())
        print('Удаление в БД выполнено')
        # Очистим поля
        self.CtgName.clear()
        self.CtgChildrens.clear()
        self.CtgParent.clear()

        # Вернём кнопки в исходное состояние
        self.CtgName.setDisabled(True)
        self.CtgParent.setDisabled(True)
        self.CtgChildrens.setDisabled(True)
        self.AcceptButton.setDisabled(True)

        self.CtgAddCheck.setDisabled(False)
        self.CtgUpdCheck.setDisabled(False)
        self.CtgDelCheck.setDisabled(False)

        print('Удаление завершено. Сброс до исходного состояния произведён.')
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
        """# Функция создания кнопки"""
        # Создали объект кнопки
        Button_obj = QtWidgets.QPushButton(text)
        # Вернули его
        return Button_obj
    # end
# end
