import aioredis
import asyncio

from loguru import logger

from config import REDIS_URL, REDIS_USERNAME, REDIS_PASSWORD


async def main() -> None:
    redis = await aioredis.from_url(
        REDIS_URL, username=REDIS_USERNAME, password=REDIS_PASSWORD, db=0
    )
    redis2 = await aioredis.from_url(
        REDIS_URL, username=REDIS_USERNAME, password=REDIS_PASSWORD, db=1
    )
    while True:
        keys = [i.decode("utf8") for i in await redis.keys()]
        keys = sorted(keys, key=lambda i: i.split('_')[-1], reverse=False)
        for key in keys:
            value = await redis.get(key)
            try:
                await redis.delete(key)
                await redis2.set(key, 'SUCCESS')
                logger.info(f'Task key={key} successfully completed')
            except Exception:
                await redis.set(key, value)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
