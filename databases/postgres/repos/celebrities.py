from datetime import date
from typing import Optional, List

from asyncpg import UniqueViolationError, ForeignKeyViolationError

from databases.postgres.queries.queries import queries
from databases.postgres.errors import DbExistenceError, DbUniqueError, DbFkError
from databases.postgres.repos.base import BaseRepository, Filter
from models.celebrities import Celebrity


class CelebritiesRepo(BaseRepository):
    async def retrieve(self, pk: int) -> Celebrity:
        record = await queries.celebrities.retrieve(self.connection, pk=pk)
        if record:
            return Celebrity(**record)
        else:
            raise DbExistenceError()

    async def list(
        self,
        tg_id: Optional[int] = None,
        username: Optional[str] = None,
        created_gte: Optional[date] = None,
        created_lte: Optional[date] = None,
    ) -> List[Celebrity]:

        fil = Filter({
            'tg_id': tg_id,
            'username': username,
            'created_gte': created_gte,
            'created_lte': created_lte
        })
        records = await self.connection.fetch(
            fil.embed(queries.celebrities.list.sql),
            *fil.params
        )
        return [Celebrity(**record) for record in records]

    async def create(self, celebrity: Celebrity) -> Celebrity:
        try:
            params = celebrity.dict()
            del params['pk']
            record = await queries.celebrities.create(self.connection, **params)
        except (UniqueViolationError, ForeignKeyViolationError) as e:
            if isinstance(e, UniqueViolationError):
                err = DbUniqueError()
            else:
                err = DbFkError()
            err.message = e.message
            raise err from e
        else:
            return Celebrity(**record)
