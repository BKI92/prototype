from typing import Any, Tuple

from asyncpg import Connection


class BaseRepository:
    def __init__(self, conn: Connection) -> None:
        self._conn = conn

    @property
    def connection(self) -> Connection:
        return self._conn


class Filter:
    def __init__(self, items: dict):
        self.__statement = []
        self.params = []
        [self.append(x, items[x]) for x in items]

    @property
    def statement(self) -> str:
        return ' AND '.join(self.__statement)

    @property
    def is_empty(self) -> bool:
        return not (
            self.params and
            self.__statement and
            len(self.params) == len(self.__statement)
        )

    def embed(self, statement: str) -> str:
        if not self.is_empty:
            return statement.replace(
                'WHERE 1=1',
                'WHERE ' + self.statement
            )
        else:
            return statement

    def append(self, key: str, value: Any):
        if value is not None:
            pos = len(self.__statement) + 1

            if key[-5:] == '_list':
                self.__statement.append(f'{key[:-5]} = ANY(${pos})')
            elif key[-5:] == '_like':
                self.__statement.append(f'{key[:-5]} LIKE ${pos}')
            elif key[-4:] == '_lte':
                self.__statement.append(f'DATE({key[:-4]}) <= ${pos}')
            elif key[-4:] == '_gte':
                self.__statement.append(f'DATE({key[:-4]}) >= ${pos}')
            else:
                self.__statement.append(f'{key} = ${pos}')

            self.params.append(value)
