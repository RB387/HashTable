from dataclasses import dataclass, field
from math import floor, fmod
from typing import Protocol, Any, Optional, List, Tuple, Callable

from lib.collision_resolver import IndexCollisionResolverProtocol


@dataclass
class BucketValue:
    __slots__ = ("key", "value", "collisions")

    key: str
    value: Any
    collisions: int


class HashBucketProtocol(Protocol):
    def add(self, key: str, value: Any):
        ...

    def get(self, key: str) -> Optional[Tuple[int, BucketValue]]:
        ...


class HashBucketFabricProtocol(Protocol):
    def new(self) -> HashBucketProtocol:
        ...


class BucketOverflow(Exception):
    ...


DEFAULT_HASH_SEED = (5 ** 0.5 - 1) / 2
DEFAULT_HASH_TABLE_SIZE = 2 ** 10
DEFAULT_HASH_MOD = 9 ** 9


@dataclass
class MultiplyHashBucket(HashBucketProtocol):
    """ Хэш таблица, работающая по методу умножения """

    collision_resolver: IndexCollisionResolverProtocol
    size: int = DEFAULT_HASH_TABLE_SIZE
    seed: float = DEFAULT_HASH_SEED

    hash_func: Callable[[str], int] = hash
    hash_mod: int = DEFAULT_HASH_MOD

    _bucket: List[Optional[BucketValue]] = field(init=False, default_factory=list)

    def __post_init__(self):
        for _ in range(self.size):
            # Заполняем пустуми значениями таблицу
            self._bucket.append(None)

    def add(self, key: str, value: Any):
        index = self._calculate_index(key)

        while not self._add(index, key, value):
            # пытаемся положить значение, пока не найдем свободную ячейку
            self._bucket[index].collisions += 1  # увеличиваем счетчик коллизий
            index = self.collision_resolver.next(index)

    def get(self, key: str) -> Optional[Tuple[int, BucketValue]]:
        index = self._calculate_index(key)

        while index < self.size:
            # Ищем значение, пока не дойдем до конца или не найдем ячейку
            cell_value = self._bucket[index]

            if cell_value is None:
                # Ячейка пуста, такого значения нет
                return None

            if key == cell_value.key:
                # Ключ совпал, значение найдено
                return index, cell_value

            # Случилась коллизия, попробуем следующую ячейку
            index = self.collision_resolver.next(index)

        return None

    def _calculate_index(self, key: str) -> Any:
        # Так как hash_func(key) может вернуть слишком большое число, берем модуль от него
        hash_value = self.hash_func(key) % self.hash_mod
        # Получаем индекс по методу умножения
        index = floor(self.size * (fmod(hash_value * self.seed, 1)))

        return index

    def _add(self, index: int, key: str, value: Any) -> bool:
        if index >= self.size:
            # Индекс слишком большой, таблица переполнена
            raise BucketOverflow

        cell_value = self._bucket[index]
        if cell_value is None:
            # ячейка пуста, можно записать значенее
            self._bucket[index] = BucketValue(key, value, 0)
            return True

        if key == cell_value.key:
            # такой ключ уже есть, достаточно перезаписать значение
            cell_value.value = value
            return True

        return False


@dataclass
class MultiplyHashBucketFabric(HashBucketFabricProtocol):
    """ Фабрика """

    collision_resolver: IndexCollisionResolverProtocol
    size: int = DEFAULT_HASH_TABLE_SIZE
    seed: float = DEFAULT_HASH_SEED

    hash_func: Callable[[str], int] = hash
    hash_mod: int = DEFAULT_HASH_MOD

    def new(self):
        return MultiplyHashBucket(
            collision_resolver=self.collision_resolver,
            size=self.size,
            seed=self.seed,
            hash_func=self.hash_func,
            hash_mod=self.hash_mod,
        )
