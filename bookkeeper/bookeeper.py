"""
    # Файл чёрного бухгалтера, который, по сути,
    # является прокладкой между внешним интерфейсом
    # и работой с БД.
    # Он не отвечает за эти действия напрямую, но передаёт
    # команды и данные туда-сюда
"""
import os
from datetime import datetime

from bookkeeper.view.View import AbstractView, View
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'bookkeeper.db')


class Bookkeeper:
    """
    # Класс чёрного бухгалтера, который, по сути,
    # является прокладкой между внешним интерфейсом
    # и работой с БД.
    # Он не отвечает за эти действия напрямую, но передаёт
    # команды и данные туда-сюда
    """

    def __init__(self,
                 view: AbstractView,
                 repository_type: type):

        # Определили вид для приложения
        self.view = view

        # Создали БД Категорий
        self.category_rep = repository_type[Category](
            db_file=db_path,
            cls=Category)
        # Вытащили все категории из БД
        self.categories = self.category_rep.get_all()
        # Установили категории в приложении
        self.view.set_categories(self.categories)
        # Задали, какой механизм отвечает за добавление категорий
        self.view.set_ctg_adder(self.add_category)
        # Задали, какой механизм отвечает за удаление категорий
        self.view.set_ctg_deleter(self.delete_category)
        # Передали механизм, отвечающий за проверку существования категории
        self.view.set_ctg_checker(self.ctg_checker)
        # Передали механизм, отвечающий за обновление категории
        self.view.set_ctg_updater(self.update_category)
        print('Вход в БД категорий обработан')

        # Создали БД Бюджета
        self.budget_rep = repository_type[Budget](
            db_file=db_path,
            cls=Budget)
        # Создали модификатор бюджета
        self.view.set_bdg_modifier(self.modify_budget)
        print('Вход в БД бюджета обработан')

        # Создали БД расходов
        self.expense_rep = repository_type[Expense](
            db_file=db_path,
            cls=Expense)
        # Обновили расходы и, заодно, бюджет (т.к. зависит от расходов)
        # Обновляем запись о расходах
        self.expenses = self.expense_rep.get_all()
        # Отправляем запись о расходах в приложеньку
        self.view.set_expenses(self.expenses)
        # Обновили запись о бюджете
        self.update_budgets()
        # добавлятор, удалятор и модификатор
        self.view.set_exp_adder(self.add_expense)
        self.view.set_exp_deleter(self.delete_expense)
        self.view.set_exp_updater(self.update_expense)
        print('Вход в БД расходов обработан')

    # end

    def start_app(self) -> None:
        """

        Кусочек для запуска приложения

        Returns
        -------

        """
        self.view.show_main_window()

    # end

    #####
    #     #   ##   ##### ######  ####   ####  #####  # ######  ####
    #        #  #    #   #      #    # #    # #    # # #      #
    #       #    #   #   #####  #      #    # #    # # #####   ####
    #       ######   #   #      #  ### #    # #####  # #           #
    #     # #    #   #   #      #    # #    # #   #  # #      #    #
    #####  #    #   #   ######  ####   ####  #    # # ######  ####

    # Проверяем, что БД категорий вообще не пуст
    def ctg_is_empty(self) -> bool:
        """

        # Проверяем, что БД категорий вообще не пуст

        Returns
        -------

        """
        if self.categories is None:
            return True
        else:
            return False
        # end

    # end

    # Проверяем, что категория существует в БД
    def ctg_checker(self, ctg_name: str) -> None:
        """

         # Проверяем, что категория существует в БД

        Parameters
        ----------
        ctg_name

        Returns
        -------

        """
        if (not self.ctg_is_empty()) and \
                (ctg_name not in [c.name for c in self.categories]):
            # Заново передадим затраты, чтобы обновить табличку
            # Отправляем запись о расходах и категориях в приложеньку
            self.view.set_expenses(self.expenses)
            self.view.set_categories(self.categories)
            print('Записи переданы в приложение')
            raise ValueError(f'Категории \'{ctg_name}\' не существует')
        # end

    # end

    # Добавляем категорию в БД и в приложеньку
    def add_category(self, name: str, parent: str, childrens: str | None = None) -> None:
        """

        # Добавляем категорию в БД и в приложеньку

        Parameters
        ----------
        name
        parent
        childrens

        Returns
        -------

        """
        print('Вошли в функцию добавления категории в БД')

        # Проверим, что такой категории ещё нет
        if not self.ctg_is_empty():
            if name in [c.name for c in self.categories]:
                raise ValueError(f'Категория \'{name}\' уже существует')
            # end
        # end
        print('Проверили, что категория существует')
        # Рассмотрим случай, когда категория дочерняя
        print('Приступаем к проверке родителя')
        if (parent is not None) & (parent != ''):
            print(f'Введён непустой родитель {parent}.')
            # Проверим, что при наличии родителя у категории,
            # такой родитель вообще есть
            if not self.ctg_is_empty():
                if parent not in [c.name for c in self.categories]:
                    raise ValueError(f'Родительской категории \'{parent}\' '
                                     f'не существует')
                # end

                parent_pk = self.category_rep.get_all(
                    where={'name': f'= \'{parent}\''})[0].pk
            else:
                parent_pk = None
            # end

        else:
            print(f'Введён пустой родитель {parent}')
            # Если категория не дочерняя (или родительская),
            # то у неё нет родителя
            parent_pk = None
        # end

        print('Родитель установлен')

        # Сформируем новый объект категории класса Category
        ctg_obj = Category(name, parent_pk)
        print('Сформирован объект')
        # Добавим его в БД
        self.category_rep.add(ctg_obj)
        print('Объект добавлен в БД')
        # Теперь, если мы хотим, чтобы у этой категории были дети,
        # то мы должны их обработать

        if (childrens is not None) & (childrens != ''):
            print('Приступаем к обработке детей')
            for child_name in childrens.split(' '):
                print(f'Рассматривается ребёнок {child_name}')
                # Проверили, что такой ребёнок существует
                self.ctg_checker(child_name)
                # Проерили, что найденный ребёнок не является родителем
                # Данной категории
                if (child_name == name) | (child_name == parent):
                    raise ValueError('Так делать нельзя!')
                # end
                print('Ребёнок не родитель для самого себя')
                # Нашли нового ребёнка
                child = self.category_rep.get_all(
                    where={'name': f'= \'{child_name}\''})[0]
                print(f'Получили класс объекта ребёнка: {str(child)}')
                # Изменили ребёнку родителя
                child.parent = ctg_obj.pk
                print('Родитель ребёнка изменён')
                # Обновили запись в БД
                self.category_rep.update(child)
                print('Запись ребёнка в БД обновлена')
            # end
            print('Дети обработаны')
        # end
        print('Приступаем к обновлению списку категорий')
        # Обновим список категорий
        self.categories = self.category_rep.get_all()
        for cats in self.categories:
            print(f'Имеется категория: {cats.name}')
        # end
        print('Список категорий отправляется в приложение')
        # Отправим новый список категорий в приложеньку
        self.view.set_categories(self.categories)
        print('Процесс добавления категории завершён')

    # end

    # Удаляем категорию из БД и приложеньки
    def delete_category(self, ctg_name: str) -> None:
        """
         # Удаляем категорию из БД и приложеньки
        Parameters
        ----------
        ctg_name

        Returns
        -------

        """
        print(f'Приступаем к удалению категории {ctg_name}')
        # Проверим, что такая категория вообще есть
        self.ctg_checker(ctg_name)
        print('Проверено наличие категории')
        # Проверим, что не пытаемся удалить вообще из пустой БД
        if self.ctg_is_empty():
            raise ValueError('Нельзя удалять из пустой таблицы!')
        # end

        # Получим объект выбранной категории (в теории он и должен быть один)
        ctg = self.category_rep.get_all(where={'name': f'= \'{ctg_name}\''})[0]
        print(f'Получен объект удаляемой категории: {str(ctg)}')
        # Необходимо обработать случаи:
        # 1. Удалённая категория - родитель. Тогда всем детям или присвоится
        # категория более старшего родителя, или None
        # 2. Удалённая категория - дитё. Тогда всем записям присвоится категория
        # родителя
        # Достанем все подкатегории удаляемой категории.
        # Для этого воспользуемся встроенным методом из класса Category
        print('Определим детей категории')
        childrens = ctg.get_subcategories(self.category_rep)

        # Рассмотрим случай, если категория дитё:
        if childrens == []:
            print('Удаляемая категория не имеет детей.\n'
                  'Перепривязка не нужна.')
        else:
            # Если мы дошли сюда, значит удаляемая категория
            # родитель для каких-то подкатегорий. Переобозначим их.
            # Учтём, что в childrens вообще вся иерархия, то есть дети,
            # их дети и т.д.. Поэтому перебором найдём только непосредственных
            # детей.
            print('Удаляемая категория - родитель. \n'
                  'Приступаем к перепривязке.')
            for child in childrens:
                print(f'Рассматриваем ребёнка: {str(child)}')
                if child.parent == ctg.pk:
                    print('Обнаружен прямой наследник.')
                    # Изменили родителя
                    child.parent = ctg.parent
                    print('Родитель изменён')
                    # Обновили запись о ребёнке в БД
                    self.category_rep.update(child)
                    print('Запись ребёнка изменена в БД')
                # end
            # end
        # end

        print('Приступаем к перепривязке затрат')
        # Переведём все затраты из удалённой категории в её родительскую.
        # Отбираем расходы удаляемой категории
        expenses_of_deleted_ctg = self.expense_rep.get_all(
            where={'category': f'= {ctg.pk}'})
        print(f'{expenses_of_deleted_ctg}')
        if (expenses_of_deleted_ctg != []) & (expenses_of_deleted_ctg is not None):
            print('Пройдена проверка на наличие объектов')
            for expense in expenses_of_deleted_ctg:
                print(f'Обнаружен расход: {str(expense)}')
                # Переназначаем категорию
                expense.category = ctg.parent
                print('Категория переназначена')
                # Обновляем запись о расходе
                self.expense_rep.update(expense)
                print('Запись расхода обновлена в БД')
            # end
        # end

        print('Приступаем к передаче новых данных')
        # Обновили расходы и, заодно, бюджет (т.к. зависит от расходов)
        # Обновляем запись о расходах
        self.expenses = self.expense_rep.get_all()
        print('Записи о расходах обновлены')
        # Отправляем запись о расходах в приложеньку
        self.view.set_expenses(self.expenses)
        print('Запись о расходах отправлена в приложение')
        # Обновили запись о бюджете
        self.update_budgets()
        print('Запись бюджета обновлена')

        # Удалим категорию из БД
        self.category_rep.delete(ctg.pk)
        print('Категория удалена из БД')
        # Обновили имеющийся список категорий
        self.categories = self.category_rep.get_all()
        print('Категории обновлены')
        # Передали в приложеньку новый список категорий
        self.view.set_categories(self.categories)
        print('Категории переданы в приложение')
        # Передали в приложеньку новый список расходов
        self.view.set_expenses(self.expenses)
        print('Расходы переданы в приложение')
        print('Удаление категории завершено')

    # end

    # Обновим категорию (СДЕЛАТЬ ЛУЧШЕ!!!)
    def update_category(self, ctg_name: str, parent: str, childrens: str = None) -> None:
        """
        # Обновим категорию (СДЕЛАТЬ ЛУЧШЕ!!!)
        Parameters
        ----------
        ctg_name
        parent
        childrens

        Returns
        -------

        """
        print('Приступаем к обновлению категории')
        if self.ctg_is_empty():
            raise ValueError('Нельзя обновлять записи пустой таблицы!')
        # end

        # Для этого удалим её и заново создадим :)
        self.delete_category(ctg_name)
        print('Категория удалена')
        self.add_category(ctg_name, parent, childrens)
        print('Категория восстановлена')
        print('Обновление категории завершено')
    # end

    #######
    #       #    # #####  ###### #    #  ####  ######  ####
    #        #  #  #    # #      ##   # #      #      #
    #####     ##   #    # #####  # #  #  ####  #####   ####
    #         ##   #####  #      #  # #      # #           #
    #        #  #  #      #      #   ## #    # #      #    #
    ####### #    # #      ###### #    #  ####  ######  ####

    # Проврека, что в БД категорий вообще что-то есть
    def exp_is_empty(self) -> bool:
        """
        # Проврека, что в БД категорий вообще что-то есть
        Returns
        -------

        """
        if self.expenses is None:
            return True
        else:
            return False
        # end

    # end

    # Добавить расход
    def add_expense(self, amount: str, ctg_name: str, comm: str = '') -> None:
        """
        # Добавить расход
        Parameters
        ----------
        amount
        ctg_name
        comm

        Returns
        -------

        """
        print('Приступаем к добавлению расхода')
        # Проверим, что в поле введено число
        try:
            amount = float(amount)
        except:
            raise ValueError('Некорректный ввод! Введите число.')
        # end
        # Проверим, что в поле введено положительное число
        if amount <= 0:
            raise ValueError('Некорректный ввод! Введите положительное число.')
        # end
        print('В поле расхода введено правильное число')
        # Проверим, что список категорий не пуст
        if self.ctg_is_empty():
            # Если пуст, то добавим введённую категорию в БД
            self.add_category(name=ctg_name, parent=None)
            print('Список категорий был пуст. Введённая категория была добавлена в БД')
        # end

        # Проверим, что введённая категория существует
        self.ctg_checker(str(ctg_name))
        print('Введённая категория существует')
        # Получим полный класс введённой категории
        ctg = self.category_rep.get_all(where={'name': f'= \'{str(ctg_name)}\''})[0]
        print('Получен полный класс введённой категории')
        print(str(ctg))
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!! Реализовать ввод даты и времени покупки! !!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Создадим объект затраты соответствующего класса
        new_expense = Expense(amount=amount, category=ctg.pk, comment=comm)
        print('Создан новый объект затраты')
        # Добавим этот объект в БД
        self.expense_rep.add(new_expense)
        print('Объект затраты добавлен в БД')
        # Обновили расходы и, заодно, бюджет (т.к. зависит от расходов)
        # Обновляем запись о расходах
        self.expenses = self.expense_rep.get_all()
        print('Получены новые расходы')
        # Отправляем запись о расходах в приложеньку
        self.view.set_expenses(self.expenses)
        print('Расходы отправлены в приложение')
        # Обновили запись о бюджете
        self.update_budgets()
        print('Бюджет обновлён')
        print('Процедура добавления расходов завершена')

    # end

    # Изменим данные о затрате
    def update_expense(self, pk: int, attrs: list[str], new_vals: list[str]) -> None:
        """
        # Изменим данные о затрате
        Parameters
        ----------
        pk
        attrs
        new_vals

        Returns
        -------

        """
        print('Приступаем к изменению расхода')
        if self.exp_is_empty():
            # Заново передадим затраты, чтобы обновить табличку
            # Отправляем запись о расходах в приложеньку
            self.view.set_expenses(self.expenses)
            print('Записи переданы в приложение')
            raise ValueError('Нельзя изменять записи пустой таблицы!')
        # end
        print('Проверили, что есть что менять')
        # Получим объект расходов, который будем изменять
        expense = self.expense_rep.get(pk)[0]
        print('Получили объект расходов, который будем менять')
        # Проверим, что что-то меняем и что не меняем ничего плохого
        if (attrs == []) | ('pk' in attrs):
            # Заново передадим затраты, чтобы обновить табличку
            # Отправляем запись о расходах в приложеньку
            self.view.set_expenses(self.expenses)
            print('Записи переданы в приложение')
            raise ValueError('Так делать нельзя!')
        # end
        print('Убедились, что всё хорошо')
        # Прогоним по позициям, которые хотим изменить
        for j in range(len(attrs)):
            # Достанем имя поля и новое значение для него
            field_name = attrs[j]
            field_val = new_vals[j]
            print(f'Сейчас меняем значение в поле {field_name} '
                  f'на величину {field_val} ')
            # Прогоним по вариантам
            if field_name == 'category':
                print('Начинаем редактировать категорию')
                # Проверим, что такая категория существует
                self.ctg_checker(field_val)
                # Получим ключ категории
                field_val = self.category_rep.get_all(
                    where={'name': f'= \'{field_val}\''})[0].pk
                print('Получили новый ключ категории')
            # end

            if field_name == 'amount':
                print('Начинаем редактировать затрату')
                # Проверим, что в поле введено число
                try:
                    field_val = float(field_val)
                except:
                    # Заново передадим затраты, чтобы обновить табличку
                    # Отправляем запись о расходах в приложеньку
                    self.view.set_expenses(self.expenses)
                    print('Записи переданы в приложение')
                    raise ValueError('Некорректный ввод! Введите число.')
                # end
                # Проверим, что в поле введено положительное число
                if field_val <= 0:
                    # Заново передадим затраты, чтобы обновить табличку
                    # Отправляем запись о расходах в приложеньку
                    self.view.set_expenses(self.expenses)
                    print('Записи переданы в приложение')
                    raise ValueError('Некорректный ввод! Введите положительное число.')
                # end
                print('Затрата введена корректная. Строка переведена во float')
            # end

            if field_name == 'expense_date':
                print('Начинаем редактировать дату затраты')
                # Проверим, что введённое время правильное
                try:
                    # Разобьём запрос на две строки, так как
                    # 'line too long' :(
                    field_val = datetime.fromisoformat(field_val).isoformat(
                        sep='T', timespec='seconds')
                except:
                    # Заново передадим затраты, чтобы обновить табличку
                    # Отправляем запись о расходах в приложеньку
                    self.view.set_expenses(self.expenses)
                    print('Записи переданы в приложение')
                    raise ValueError('Неправильный формат даты.')
                # end
                print('Дату ввели корректно. Передаём дальше')
            # end

            # Обновили значение поля
            setattr(expense, field_name, field_val)
            print('Значение поля обновлено')
        # end

        # Обновим значение поля с датой обновления
        setattr(expense, 'added_date', datetime.now().isoformat()[:19])
        print('Обновили поле с датой обновления записи')
        # Обновили расход в БД
        self.expense_rep.update(expense)
        print('Данные в БД обновлены')
        # Обновили расходы и, заодно, бюджет (т.к. зависит от расходов)
        # Обновляем запись о расходах
        self.expenses = self.expense_rep.get_all()
        print('Записи в классе обновлены')
        # Отправляем запись о расходах в приложеньку
        self.view.set_expenses(self.expenses)
        print('Записи переданы в приложение')
        # Обновили запись о бюджете
        self.update_budgets()
        print('бюджет обновлён')
        print('Обновление данных расхода завершено')

    # end

    # Удаляем запись о расходах
    def delete_expense(self, pk: str) -> None:
        """
        # Удаляем запись о расходах
        Parameters
        ----------
        pk

        Returns
        -------

        """
        print('Приступаем к удалению данных из расходов')
        if self.exp_is_empty():
            raise ValueError('Нельзя удалять записи пустой таблицы!')
        # end
        try:
            pk = int(pk)
        except:
            raise ValueError('Некорректный ввод!')
        # end
        if not isinstance(pk, int):
            raise ValueError('Что-то не так с форматом!')
        # end
        # Проверим, что такая запись есть в БД
        exp_for_delete = self.expense_rep.get(pk)
        print(exp_for_delete)
        if (exp_for_delete == []) | (exp_for_delete is None):
            raise ValueError('Такой записи нет - удалять нечего!')
        # end

        # Удалили запись из БД
        self.expense_rep.delete(pk)

        # Обновили расходы и, заодно, бюджет (т.к. зависит от расходов)
        # Обновляем запись о расходах
        self.expenses = self.expense_rep.get_all()
        # Отправляем запись о расходах в приложеньку
        self.view.set_expenses(self.expenses)
        # Обновили запись о бюджете
        self.update_budgets()
        print('Расход удалён')

    # end

    #####
    #     # #    # #####   ####  ###### #####
    #     # #    # #    # #    # #        #
    ######  #    # #    # #      #####    #
    #     # #    # #    # #  ### #        #
    #     # #    # #    # #    # #        #
    ######   ####  #####   ####  ######   #

    # Обновляем информацию о бюджете везде
    def update_budgets(self) -> None:
        """
        # Обновляем информацию о бюджете везде
        Returns
        -------

        """
        print('Приступаем к обновлению бюджета')
        # Проверим, что записи бюджета вообще есть
        if self.budget_rep.get_all() is None:
            print('Активных записей нет')
        else:
            # Прогоняем все категории бюджетов
            print('Найдены активные записи')
            for budget in self.budget_rep.get_all():
                # Обновили трату в бюджете
                budget.update_spented_sum(self.expense_rep)
                print('Трата в бюджете обновлена')
                # Обновили запись в БД
                self.budget_rep.update(budget)
                print('Обновлена запись в БД')
            # end
        # end
        # Вытащили обновлённые бюджеты
        self.budgets = self.budget_rep.get_all()
        print('Записи бюджетов в классе обновлены')
        # Обновили вид записей в приложении
        self.view.set_budgets(self.budgets)
        print('Записи бюджетов отправлены в приложение')

    # end

    # Модифицируем бюджет (т.е. изменяем данные)
    def modify_budget(self, pk: int | None, new_budget_val: str, time: str) -> None:
        """
        # Модифицируем бюджет (т.е. изменяем данные)
        Parameters
        ----------
        pk
        new_budget_val
        time

        Returns
        -------

        """
        if new_budget_val == '':
            print('Удалена запись о бюджете. Удаляем информацию')
            if (pk is not None) & (pk != ''):
                self.budget_rep.delete(pk)
                print('Запись удалена')
            # end
            self.update_budgets()
            print('Данные о бюджетах обновлены')
        else:
            # Проверим, что ввод вообще числовой
            try:
                new_budget_val = float(new_budget_val)
            except ValueError:
                # Обновляем информацию о бюджете, чтобы
                # сбросить введённый в таблицу сусор
                self.update_budgets()
                print('Записи бюджета обновлены')
                raise ValueError('Неправильный ввод! Введите число.')
            # end
            # Проверим на положительность
            if new_budget_val < 0:
                # Обновляем информацию о бюджете, чтобы
                # сбросить введённый в таблицу сусор
                self.update_budgets()
                print('Записи бюджета обновлены')
                raise ValueError('Неправильный ввод! Введите положительное число.')
            # end

            print('Ввод корректен')

            # Проверим, что такая запись вообще существует, а
            # если не существует, то создадим её
            if (pk is None) | (pk == ''):
                # Создадим новую запись
                budget = Budget(budget=new_budget_val, time=time)
                print('Создана новая запись')
                # Передадим запись в БД
                self.budget_rep.add(budget)
                print('Запись добавлена в БД')
            else:
                # Получим запись по ключу
                budget = self.budget_rep.get(pk)[0]
                print('Запись по ключу получена')
                # Вытащили данные и обновили их
                budget.budget = new_budget_val
                # Обновили запись в бюджете
                self.budget_rep.update(budget)
                print('Запись в БД обновлена')
            # end
        self.update_budgets()
    # end
# end

# Штука, чтобы это точно-точно работало
if __name__ == '__main__':
    view = View()
    bookkeeper_app = Bookkeeper(view, SQLiteRepository)
    bookkeeper_app.start_app()
# end
