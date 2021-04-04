from dataclasses import dataclass, field
from typing import List, Any, Optional, Tuple

from lib.hash_bucket import (
    HashBucketFabricProtocol,
    HashBucketProtocol,
    BucketOverflow,
    BucketValue,
)


class HashTableProtocol(HashBucketProtocol):
    ...


@dataclass
class HashTable(HashTableProtocol):
    """ Хэш таблица, расширяющаяся по степени заполнености """

    bucket_fabric: HashBucketFabricProtocol

    _buckets: List[HashBucketProtocol] = field(init=False, default_factory=list)

    def __post_init__(self):
        # При инициализации создаем первую хэш таблицу
        self._buckets.append(self.bucket_fabric.new())

    def add(self, key: str, value: Any):
        # Берем последнюю на данный момент хэш таблицу
        bucket = self._buckets[-1]

        try:
            bucket.add(key, value)
        except BucketOverflow:
            # Если переполнили таблицу, создаем новую и кладем значение туда
            bucket = self.bucket_fabric.new()
            self._buckets.append(bucket)
            bucket.add(key, value)

    def get(self, key: str) -> Optional[Tuple[int, BucketValue]]:
        for bucket in self._buckets:
            # Ищем значение во всех созданных таблицах
            value = bucket.get(key)

            if value is not None:
                return value

        return None
