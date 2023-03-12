"""Класс для простого создания и настройки выпадающего списка"""
from PyQt6 import QtWidgets


# Класс выпадающего списка
class EasyComboBox(QtWidgets.QComboBox):
    """Класс для простого создания и настройки выпадающего списка"""

    def __init__(self, cur_text: str = 'Empty', *args, **kwargs):
        # Передадим всё лишнее родителю
        super().__init__(*args, **kwargs)
        # Сделаем редактируемым (а лучше не будем)
        # self.setEditable(True)
        self.clear()
        # Заполним пустотами, просто потому что можем
        self.set_items()
    # end

    # Составляем начинку выпадающего списка
    def set_items(self, text_for_items: list[str] = ['empty']) -> None:
        """
        # Составляем начинку выпадающего списка
        Parameters
        ----------
        text_for_items

        Returns
        -------

        """
        # Очистим содержимое выпадающего списка
        self.clear()
        print('В теории, список должен был очиститься')
        super().clear()
        print('Совсем мощно должен был очиститься')
        # Проверим, что на входе что-то есть и оно str
        if (isinstance(text_for_items, str)) | (text_for_items == []):
            raise ValueError('Неверный ввод!')
        # end

        # Составим его начинку
        for name in text_for_items:
            print(f'Добавлено окошко {name}')
            self.addItem(name)
        # end
# end
