from cli import MainActivity
from lib.collision_resolver import LinearIndexCollisionResolver
from lib.hash_bucket import MultiplyHashBucket

LINEAR_COLLISION_RESOLVER_STEP = 4


def main():
    hash_table = MultiplyHashBucket(
        collision_resolver=LinearIndexCollisionResolver(
            step=LINEAR_COLLISION_RESOLVER_STEP,
        ),
    )

    activity = MainActivity(hash_table)
    activity.start()


if __name__ == "__main__":
    main()
