"""
Модель категории расходов
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, Any

from ..repository.abstract_repository import AbstractRepository


@dataclass
class Category:
    """
    Категория расходов, хранит название в атрибуте name и ссылку (id) на
    родителя (категория, подкатегорией которой является данная) в атрибуте parent.
    У категорий верхнего уровня parent = None
    """
    name: str = 'Empty'
    parent: int | None = None
    pk: int = 0

    def get_parent(self, repo: AbstractRepository['Category']) -> 'Category | None':
        """
        Получить родительскую категорию в виде объекта Category
        Если метод вызван у категории верхнего уровня, возвращает None

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Returns
        -------
        Объект класса Category или None
        """
        if self.parent is None:
            return None
        return repo.get(self.parent)

    def get_all_parents(self,
                        repo: AbstractRepository['Category']
                        ) -> Iterator['Category']:
        """
        Получить все категории верхнего уровня в иерархии.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category от родителя и выше до категории верхнего уровня
        """
        parent = self.get_parent(repo)
        if parent is None:
            return
        yield parent
        yield from parent.get_all_parents(repo)

    def get_subcategories(self,
                          repo: AbstractRepository['Category']
                          ) -> Iterator['Category']:
        """
        Получить все подкатегории из иерархии, т.е. непосредственные
        подкатегории данной, все их подкатегории и т.д.

        Parameters
        ----------
        repo - репозиторий для получения объектов

        Yields
        -------
        Объекты Category, являющиеся подкатегориями разного уровня ниже данной.
        """

        def get_children(graph: dict[int | None, list['Category']],
                         root: int) -> Iterator['Category']:
            """ dfs in graph from root """
            for x in graph[root]:
                yield x
                yield from get_children(graph, x.pk)

        subcats = defaultdict(list)
        for cat in repo.get_all():
            subcats[cat.parent].append(cat)
        return get_children(subcats, self.pk)

    @classmethod
    def create_from_tree(
            cls,
            tree: list[tuple[str, str | None]],
            repo: AbstractRepository['Category']) -> list['Category']:
        """
        Создать дерево категорий из списка пар "потомок-родитель".
        Список должен быть топологически отсортирован, т.е. потомки
        не должны встречаться раньше своего родителя.
        Проверка корректности исходных данных не производится.
        При использовании СУБД с проверкой внешних ключей, будет получена
        ошибка (для sqlite3 - IntegrityError). При отсутствии проверки
        со стороны СУБД, результат, возможно, будет корректным, если исходные
        данные корректны за исключением сортировки. Если нет, то нет.
        "Мусор на входе, мусор на выходе".

        Parameters
        ----------
        tree - список пар "потомок-родитель"
        repo - репозиторий для сохранения объектов

        Returns
        -------
        Список созданных объектов Category
        """
        created: dict[str, Category] = {}
        for child, parent in tree:
            cat = cls(child, created[parent].pk if parent is not None else None)
            repo.add(cat)
            created[child] = cat
        return list(created.values())

    # Оформим красивый вывод для отладки
    def __str__(self) -> str:
        return f'pk = {self.pk}; name = {self.name}; parent = {self.parent};'
    # end

    # Напишем процедуру сравнения двух элементов класса, так как иначе сравнение идёт
    # по адресу в памяти или ещё чему-то не тому
    def __eq__(self, check: Any) -> bool:
        # Проверим сначала, что совпадают типы
        if not isinstance(check, Category):
            return NotImplemented
        else:
            FTans = ((self.pk == check.pk) and
                     (self.name == check.name) and
                     (self.parent == check.parent))
            return FTans
        # end
    # end
