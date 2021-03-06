import aioredis
import asyncio

from aiogram import Bot, Dispatcher
from loguru import logger

from config import REDIS_URL, REDIS_USERNAME, REDIS_PASSWORD, BOT_TOKEN
from databases.postgres import get_db_conn
from databases.postgres.repos.users import UsersRepo

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def main() -> None:
    redis = await aioredis.from_url(
        REDIS_URL, username=REDIS_USERNAME, password=REDIS_PASSWORD, db=1
    )
    conn = await get_db_conn()
    while True:
        keys = [i.decode("utf8") for i in await redis.keys()]
        keys = sorted(keys, key=lambda i: i.split('_')[-1], reverse=False)
        users_repo = UsersRepo(conn)
        users = await users_repo.list()
        users_lookup = {i.pk: i.tg_id for i in users}
        for key in keys:
            value = await redis.get(key)
            try:
                await redis.delete(key)
                tg_id = users_lookup.get(int(key.split('_')[0]))
                logger.info(f'TG ID = {tg_id}')
                await bot.send_message(tg_id, value.decode('utf-8'))
                logger.info(f'Task key={key} successfully sent. {value.decode("utf-8")}')
            except Exception as e:
                logger.error(e)
                await redis.set(key, value)
        await redis.close()

if __name__ == '__main__':
    logger.info('Start responder')
    asyncio.get_event_loop().run_until_complete(main())
