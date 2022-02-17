from datetime import date
from typing import Optional, List

from asyncpg import UniqueViolationError, ForeignKeyViolationError

from databases.postgres.queries.queries import queries
from databases.postgres.errors import DbUniqueError, DbFkError
from databases.postgres.repos.base import BaseRepository, Filter
from models.messages import Message


class MessagesRepo(BaseRepository):
    async def list(
        self,
        user_pk: Optional[int] = None,
        celebrity_pk: Optional[int] = None,
        created_gte: Optional[date] = None,
        created_lte: Optional[date] = None,
    ) -> List[Message]:

        fil = Filter({
            'user_pk': user_pk,
            'celebrity_pk': celebrity_pk,
            'created_gte': created_gte,
            'created_lte': created_lte
        })
        records = await self.connection.fetch(
            fil.embed(queries.messages.list.sql),
            *fil.params
        )
        return [Message(**record) for record in records]

    async def create(self, message: Message) -> Message:
        try:
            params = message.dict()
            record = await queries.messages.create(self.connection, **params)
        except (UniqueViolationError, ForeignKeyViolationError) as e:
            if isinstance(e, UniqueViolationError):
                err = DbUniqueError()
            else:
                err = DbFkError()
            raise err from e
        else:
            return Message(**record)

