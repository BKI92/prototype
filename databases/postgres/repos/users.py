from datetime import date
from typing import Optional, List

from asyncpg import UniqueViolationError, ForeignKeyViolationError

from databases.postgres.queries.queries import queries
from databases.postgres.errors import DbExistenceError, DbUniqueError, DbFkError
from databases.postgres.repos.base import BaseRepository, Filter
from models.users import User


class UsersRepo(BaseRepository):
    async def retrieve(self, pk: int) -> User:
        conn = await self.connection
        record = await queries.users.retrieve(conn, pk=pk)
        if record:
            return User(**record)
        else:
            raise DbExistenceError()

    async def list(
        self,
        tg_id: Optional[int] = None,
        username: Optional[str] = None,
        created_gte: Optional[date] = None,
        created_lte: Optional[date] = None,
    ) -> List[User]:
        conn = self.connection
        fil = Filter({
            'tg_id': tg_id,
            'username': username,
            'created_gte': created_gte,
            'created_lte': created_lte
        })
        records = await conn.fetch(
            fil.embed(queries.users.list.sql),
            *fil.params
        )
        return [User(**record) for record in records]

    async def create(self, user: User) -> User:
        try:
            params = user.dict()
            del params['pk']
            record = await queries.users.create(self.connection, **params)
        except (UniqueViolationError, ForeignKeyViolationError) as e:
            if isinstance(e, UniqueViolationError):
                err = DbUniqueError()
            else:
                err = DbFkError()
            err.message = e.message
            raise err from e
        else:
            return User(**record)
