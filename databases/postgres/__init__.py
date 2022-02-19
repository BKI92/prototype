import json

import asyncpg
from asyncpg import Connection
from loguru import logger

from config import PG_DATABASE_URL


async def get_db_conn() -> Connection:
    if not PG_DATABASE_URL:
        logger.critical('DATABASE_URL is empty, try to run script from project root')
        exit(1)

    try:
        conn = await asyncpg.connect(PG_DATABASE_URL)
        await conn.set_type_codec(
            'jsonb',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        return conn

    except ConnectionRefusedError:
        logger.critical(f'Cannot connect to database on url={PG_DATABASE_URL}')
        exit(2)

    except Exception as e:
        logger.critical(e)
        exit(3)
