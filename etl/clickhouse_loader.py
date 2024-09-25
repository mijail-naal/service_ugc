import backoff

from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError
from utils.handler import backoff_hadler


class ClickhouseLoader:
    def __init__(self, client: Client, cluster: str) -> None:
        self.client = client
        self.cluster = cluster

    @backoff.on_exception(backoff.expo, ConnectionRefusedError, on_backoff=backoff_hadler)
    @backoff.on_exception(backoff.expo, NetworkError, on_backoff=backoff_hadler)
    def _execute_query(self, query) -> None:
        self.client.execute(query)

    def _create_database(self, database: str) -> None:
        self._execute_query(
            f'CREATE DATABASE IF NOT EXISTS {database} ON CLUSTER {self.cluster}'
        )

    def _create_table(self, statement: str, database: str) -> None:
        query = statement.format(database=database)
        self._execute_query(query)

    def start(self, database: str, statement: str) -> str:
        self._create_database(database)
        self._create_table(statement, database)
        return 'Database and table created'

    def load(self, database: str, table: str, columns: str, values: str) -> str:
        query = f'INSERT INTO {database}.{table} ({columns}) VALUES '
        query += values

        if not values:
            return 'No values found'
        self._execute_query(query)
        return 'Data loaded'

    def drop_table(self, name: str) -> str:
        query = f'DROP TABLE {name};'
        self._execute_query(query)
        return f'Table {name} droped'

    def close(self) -> bool:
        self.client.disconnect()
        self.client.disconnect_connection()
        return True
