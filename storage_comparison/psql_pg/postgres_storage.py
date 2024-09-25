# import sys

from time import time

from psycopg2.extensions import connection as _connection, cursor as _cursor

# sys.path.append('..')
from utils.abstract import AbstractStorage
from utils.data_generator import DataGenerator


class PostgresStorage(AbstractStorage):
    def __init__(self, conn: _connection, cursor: _cursor, generator: DataGenerator) -> None:
        self.conn = conn
        self.cursor = cursor
        self.generator = generator

    def _execute_query(self, query: str) -> float:
        start = time()
        self.cursor.execute(query)
        end = time()
        return end - start

    def _execute_and_commit(self, query: str, data='') -> None:
        self.cursor.execute(query, data)
        self.conn.commit()

    def create_table(self, query: str, table: str) -> str:
        query = query % table
        self._execute_and_commit(query)
        return query

    def drop_table(self, name: str) -> None:
        query = f'DROP TABLE {name};'
        self._execute_and_commit(query)

    def add(self, query: str, table: str, total: int, batch: int) -> float:
        start = time()
        for q in self.generator.add_data(total, batch, query, table):
            self.cursor.execute(q)
        self.conn.commit()
        end = time()
        return end - start

    def read(self, query: str, table: str) -> float:
        query = query % table
        result = self._execute_query(query)
        return result
