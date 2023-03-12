from bookkeeper.repository.sqlite_repository import SQLiteRepository
import pytest
import os.path
import datetime
from dataclasses import dataclass, field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'for_tests_db.db')

#Какая-то штуко, которая может вернуть что-то
@pytest.fixture
def custom_class():
    # Это класс, который описывает возможные случаи
    # классов, что могут вноситься в БД
    class Custom():
        somestr: str
        val: float
        somedate: str
        pk: int = 0

        def __init__(self, str_in: str = 'test', val_in: float = 2.718281828459045, dtdt_in: str = str(datetime.datetime.now())):
            self.somestr = str_in
            self.val = val_in
            self.somedate = dtdt_in
        # end

        #Оформим красивый вывод для отладки
        def __str__(self) -> str:
            return f'pk = {self.pk}; somestr = {self.somestr}; val = {self.val}; somedate = {self.somedate};'
        # end

        #Напишем процедуру сравнения двух элементов класса, так как иначе сравнение идёт
        #по адресу в памяти или ещё чему-то не тому
        def __eq__(self, check) -> bool:
            #Проверим сначала, что совпадают типы
            if (not isinstance(check, Custom)):
                return NotImplemented
            else:
                FTans = ((self.pk == check.pk) & (self.somestr == check.somestr) and (self.val == check.val) and (self.somedate == check.somedate))
                return FTans
            # end
        # end

    # end
    return Custom
# end

#Какая-то штуко, которая может вернуть что-то
@pytest.fixture
def repo(custom_class):
    return SQLiteRepository(db_path, custom_class)
# Для краткости заранее создаём обращение к БД

# Проверяем: добавление, обращение, обновление, удаление
def test_crud(repo, custom_class):
    #Создали объект
    obj = custom_class()
    #Загнали в БД и посмотрели его индекс
    pk = repo.add(obj)
    #Проверили, что ???????
    assert obj.pk == pk
    #Проверили, что по индексу можем достать объект
    assert repo.get(pk)[0] == obj
    #Создали другой объект
    obj2 = custom_class(0, 'testtest', 3.1415)
    #Присвоили объекту ключ старого объекта
    obj2.pk = pk
    # Обновили объект obj объектом obj2
    repo.update(obj2)
    #Проверили, что обновление прошло
    assert repo.get(pk)[0] == obj2
    #Удалили объект
    repo.delete(pk)
    #Проверили, что удалили объект
    assert repo.get(pk) is None
    #На всякий случай очистили таблицу
    repo.delete_all()
# end

def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)

def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)

def test_cannot_delete_unexistent(repo):
    repo.delete_all()
    with pytest.raises(KeyError):
        repo.delete(1)

def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)

def test_get_all(repo, custom_class):
    #Перед выполнением очистим
    repo.delete_all()
    objects = []
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects

    #После выполнения очистим
    repo.delete_all()
# end

def test_delete_all(repo, custom_class):
    objects = []
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    # end
    # После выполнения очистим
    repo.delete_all()
    assert repo.get_all() is None
# end

def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.val = i
        o.somestr = f'text {i}'
        repo.add(o)
        objects.append(o)
    # end
    assert repo.get_all({'val': '= 0'})[0] == objects[0]
    assert repo.get_all({'somestr': '= \'text 1\'', 'val': '< 4'})[0] == objects[1]
    assert repo.get_all({'val': '< 3'}) == objects[0:3:1]
# end