# import sys

from time import time

from clickhouse_driver import Client

# sys.path.append('..')
from utils.abstract import AbstractStorage
from utils.data_generator import DataGenerator


class ClickhouseStorage(AbstractStorage):
    def __init__(self, client: Client, generator: DataGenerator) -> None:
        self.client = client
        self.generator = generator

    def _execute_query(self, query: str) -> float:
        start = time()
        self.client.execute(query)
        end = time()
        return end - start

    def create_table(self, query: str, table: str) -> str:
        query = query % table
        self._execute_query(query)
        return query

    def drop_table(self, name: str) -> None:
        query = f'DROP TABLE {name};'
        self._execute_query(query)

    def add(self, query: str, table: str, total: int, batch: int) -> float:
        start = time()
        for q in self.generator.add_data(total, batch, query, table):
            self.client.execute(q)
        end = time()
        return end - start

    def read(self, query: str, table: str) -> float:
        query = query % table
        result = self._execute_query(query)
        return result

    def close(self):
        self.client.disconnect()
        self.client.disconnect_connection()
        return True
