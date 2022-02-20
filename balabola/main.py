import json

import aioredis
import asyncio

from aiobalaboba import balaboba
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
            value = json.loads(value).get('text', '')
            try:
                await redis.delete(key)
                message = await balaboba(value) or 'Empty'
                await redis2.set(key, message)
                logger.info(f'Task key={key} successfully completed')
            except Exception as e:
                logger.error(e)
                await redis.set(key, value)
        await redis.close()
        await redis2.close()

if __name__ == '__main__':
    logger.info('Start balabola')
    asyncio.get_event_loop().run_until_complete(main())
