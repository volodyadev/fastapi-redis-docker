import redis

from app.settings import settings


def create_redis():
    return redis.ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True,
        password=settings.REDIS_PASSWORD,
    )


pool = create_redis()
