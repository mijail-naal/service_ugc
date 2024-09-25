from uuid import uuid4
from random import randint


class DataGenerator:
    def generate_data(self, query: str, table: str, rows: int) -> int:
        query = query % table
        for _ in range(rows):
            query += f"('{str(uuid4())}', '{str(uuid4())}', {randint(100000000, 1000000000)}), "
        return query.rstrip(', ')

    def generate_values(self, rows: int) -> int:
        data = [(str(uuid4()), str(uuid4()), randint(100000000, 1000000000)) for _ in range(rows)]
        return data

    def add_data(self, total, size, query, table, only_values: bool = None):
        times = total // size + 1
        if total % size == 0:
            times = total // size

        for _ in range(times):
            if not only_values:
                data = self.generate_data(query, table, size)
            else:
                data = self.generate_values(size)
            yield data


if __name__ == '__main__':
    PSQL_INSERT = 'INSERT INTO %s (user_id, movie_id, viewed_frame) VALUES '

    dg = DataGenerator()

    # Section to check the returned data

    for i in dg.add_data(10, 2, PSQL_INSERT, 'views'):
        # Testing generate_data()
        print(i)

    for i in dg.add_data(10, 2, PSQL_INSERT, 'views', only_values=True):
        # Testing generate_values()
        print(i)
