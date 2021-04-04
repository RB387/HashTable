from lib import HashTable
from lib.collision_resolver import LinearIndexCollisionResolver
from lib.hash_bucket import MultiplyHashBucketFabric, BucketValue


def test_simple_hash_table():
    hash_table = HashTable(
        bucket_fabric=MultiplyHashBucketFabric(
            collision_resolver=LinearIndexCollisionResolver(step=1),
            size=1,
        ),
    )

    hash_table.add('my_key', 'my_value')
    index, result = hash_table.get('my_key')

    assert index == 0
    assert result == BucketValue(key='my_key', value='my_value', collisions=0)


def test_resize_hash_table():
    hash_table = HashTable(
        bucket_fabric=MultiplyHashBucketFabric(
            collision_resolver=LinearIndexCollisionResolver(step=1),
            size=1,
        ),
    )

    hash_table.add('my_key', 'my_value')
    hash_table.add('new_key', 'my_value')

    assert len(hash_table._buckets) == 2

    index, result = hash_table.get('my_key')
    assert index == 0
    assert result == BucketValue(key='my_key', value='my_value', collisions=1)

    index, result = hash_table.get('new_key')
    assert index == 0
    assert result == BucketValue(key='new_key', value='my_value', collisions=0)
