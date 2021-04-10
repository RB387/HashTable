import pytest

from lib.collision_resolver import LinearIndexCollisionResolver
from lib.hash_bucket import MultiplyHashBucket, BucketValue, BucketOverflow


def test_simple_multiply_hash_bucket():
    bucket = MultiplyHashBucket(
        collision_resolver=LinearIndexCollisionResolver(1),
        size=1,
    )

    bucket.add('my_key', 'my_value')
    index, result = bucket.get('my_key')

    assert index == 0
    assert result == BucketValue(key='my_key', value='my_value', collisions=0)

    bucket.add('my_key', 'new_value')
    _, result = bucket.get('my_key')
    assert result == BucketValue(key='my_key', value='new_value', collisions=0)

    result = bucket.get('no_key')
    assert result is None


def test_collision_multiply_hash_bucket():
    bucket = MultiplyHashBucket(
        collision_resolver=LinearIndexCollisionResolver(1),
        size=1,
    )

    bucket.add('my_key', 'my_value')

    with pytest.raises(BucketOverflow):
        bucket.add('new_key', 'my_value')

    _, result = bucket.get('my_key')
    assert result.collisions == 1


def test_multiple_add_multiply_hash_bucket(mock_hash):
    bucket = MultiplyHashBucket(
        hash_func=mock_hash,
        collision_resolver=LinearIndexCollisionResolver(1),
        size=10,
    )

    for idx in range(5):
        bucket.add(f'key{idx}', f'value{idx}')

    assert bucket._bucket == [
        None,
        BucketValue(key='key1', value='value1', collisions=0),
        None,
        None,
        BucketValue(key='key2', value='value2', collisions=0),
        BucketValue(key='key4', value='value4', collisions=0),
        BucketValue(key='key0', value='value0', collisions=1),
        BucketValue(key='key3', value='value3', collisions=0),
        None,
        None,
    ]

    index, result = bucket.get('key2')
    assert index == 4
    assert result == BucketValue(key='key2', value='value2', collisions=0)
