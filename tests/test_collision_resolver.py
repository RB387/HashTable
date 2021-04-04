import pytest

from lib.collision_resolver import LinearIndexCollisionResolver


@pytest.mark.parametrize(
    'index, step, expected_next_index',
    (
        (1, 4, 5),
        (5, 4, 9),
        (0, 1, 1),
    ),
)
def test_linear_collision_resolver(index, step, expected_next_index):
    resolver = LinearIndexCollisionResolver(step)

    assert resolver.next(index) == expected_next_index
