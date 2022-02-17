import json
import time
from typing import Tuple

import aioredis

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from loguru import logger

from config import BOT_TOKEN, REDIS_URL, REDIS_USERNAME, REDIS_PASSWORD
from databases.postgres import get_db_conn
from databases.postgres.errors import DbFkError
from databases.postgres.repos.celebrities import CelebritiesRepo
from databases.postgres.repos.messages import MessagesRepo
from databases.postgres.repos.users import UsersRepo
from models.messages import Message
from models.users import User

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def get_data_from_message(text: str) -> Tuple[int, str]:
    resp = text.split('//')
    if len(resp) < 2:
        return 0, ''
    else:
        return int(resp[-1]), resp[0]


@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    conn = await get_db_conn()
    users_repo = UsersRepo(conn)
    user = User(
        pk=0,
        tg_id=msg.from_user.id,
        username=msg.from_user.username,
        description='Additional Info '
    )
    users = await users_repo.list(tg_id=msg.from_user.id)
    if not users:
        created_user = await users_repo.create(user)
        logger.info(f'Created {created_user.dict()}')
        await msg.reply("Привет!\nНапиши мне что-нибудь!")

    await conn.close()


@dp.message_handler(commands=['help'])
async def process_help_command(msg: types.Message):
    message = 'Send message in format: your message //celebrity_pk \n' \
             'You may see all celebrities with command /cel'
    await bot.send_message(msg.from_user.id, message)


@dp.message_handler(commands=['cel'])
async def process_help_command(msg: types.Message):
    result = 'Choose celebrity: \n'
    conn = await get_db_conn()
    cel_repo = CelebritiesRepo(conn)
    res = await cel_repo.list()
    await bot.send_message(msg.from_user.id, result+'\n'.join([f'{i.pk} - {i.name}' for i in res]))
    await conn.close()


@dp.message_handler()
async def create_task(msg: types.Message):
    redis = await aioredis.from_url(
        REDIS_URL, username=REDIS_USERNAME, password=REDIS_PASSWORD, db=0
    )
    conn = await get_db_conn()

    try:
        msgs_repo = MessagesRepo(conn)
        users_repo = UsersRepo(conn)

        users = await users_repo.list(tg_id=msg.from_user.id)
        user_pk = users[0].pk
        cel_pk, text = get_data_from_message(msg.text)
        message = Message(title=text, user_pk=user_pk, celebrity_pk=cel_pk)
        await msgs_repo.create(message)
        task_key = f'{user_pk}_{int(time.time())}'
        await redis.set(task_key, json.dumps({'user_pk': user_pk, 'text': text, 'cel_pk': cel_pk}))
        # await bot.send_message(msg.from_user.id, str(int(time.time())))
        logger.info(f'Task key={task_key} successfully created')
    except DbFkError:
        logger.debug('Error in celebrity fk key')
    except Exception as e:
        logger.error(e)
    finally:
        await conn.close()
        await redis.close()


if __name__ == '__main__':
    executor.start_polling(dp)
