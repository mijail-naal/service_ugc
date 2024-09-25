# import sys

from time import time

from vertica_python.vertica.connection import Connection
from vertica_python.vertica.cursor import Cursor

# sys.path.append('..')
from utils.abstract import AbstractStorage
from utils.data_generator import DataGenerator


class VerticaStorage(AbstractStorage):
    def __init__(self, conn: Connection, cursor: Cursor, generator: DataGenerator) -> None:
        self.conn = conn
        self.cursor = cursor
        self.generator = generator

    def _execute_query(self, query: str) -> int:
        start = time()
        self.cursor.execute(query)
        self.conn.commit()
        end = time()
        return end - start

    def create_table(self, query: str, table: str) -> str:
        query = query % table
        self._execute_query(query)
        return query

    def drop_table(self, name: str) -> None:
        query = f'DROP TABLE {name};'
        self._execute_query(query)

    def add(self, query: str, table: str, total: int, batch: int) -> int:
        query = query % table + '(%s, %s, %s);'
        start = time()
        for data in self.generator.add_data(total, batch, query, table, only_values=True):
            self.cursor.executemany(query, data)
        self.conn.commit()
        end = time()
        return end - start

    def read(self, query: str, table: str) -> int:
        query = query % table
        result = self._execute_query(query)
        return result
