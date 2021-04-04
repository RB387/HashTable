from dataclasses import dataclass
from typing import Protocol


class IndexCollisionResolverProtocol(Protocol):
    """ Интерфейс для алгоритма разрешения коллизий """

    def next(self, index: int) -> int:
        ...


@dataclass
class LinearIndexCollisionResolver(IndexCollisionResolverProtocol):
    """ Алгоритм линейного разрешения коллизий """

    step: int

    def next(self, index: int) -> int:
        return index + self.step
