from uuid import uuid4
from random import randint

from typing import Any


class DataGenerator:
    def generate_data(self, query: str, table: str, rows: int) -> str:
        query = query % table
        for _ in range(rows):
            query += f"('{str(uuid4())}', '{str(uuid4())}', {randint(100000000, 1000000000)}), "
        return query.rstrip(', ')

    def generate_values(self, rows: int) -> list[tuple[str, str, int]]:
        data = [(str(uuid4()), str(uuid4()), randint(100000000, 1000000000)) for _ in range(rows)]
        return data

    def add_data(self, total: int, size: int, query: str, table: str, only_values: bool = False) -> Any:
        times = total // size + 1
        if total % size == 0:
            times = total // size

        for _ in range(times):
            if not only_values:
                data = self.generate_data(query, table, size)
            else:
                data = self.generate_values(size)
            yield data


class MongoDataGenerator:
    def generate_data(self, rows: int) -> list[dict[str, object]]:
        return [
            {'user_id': str(uuid4()), 'movie_id': str(uuid4()), 'viewed_frame': randint(100000000, 1000000000)}
            for _ in range(rows)
        ]

    def add_data(self, total: int, size: int):
        times = total // size + 1
        if total % size == 0:
            times = total // size

        for _ in range(times):
            data = self.generate_data(size)
            yield data


if __name__ == '__main__':
    PSQL_INSERT = 'INSERT INTO %s (user_id, movie_id, viewed_frame) VALUES '

    dg = DataGenerator()

    # Section to check the returned data

    for d in dg.add_data(10, 2, PSQL_INSERT, 'views'):
        # Testing generate_data()
        print(d)

    for v in dg.add_data(10, 2, PSQL_INSERT, 'views', only_values=True):
        # Testing generate_values()
        print(v)
