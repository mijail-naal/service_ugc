import psycopg2

from contextlib import closing

from config.settings import pg
from psql_pg.postgres_storage import PostgresStorage
from utils.queries import PSQL_CREATE_TABLE, INSERT, SELECT
from utils.data_generator import DataGenerator


def metrics(res, action, rows, batch):
    result = f"""
    PostgreSQL {action} results:

    Total rows               |Batch                     | Average per {action:<12} | Total execution time
    -------------------------|--------------------------|--------------------------|----------------------
    {rows:<24} | {batch:<24} | {res / rows:<24} | {res:<24}
    """
    return result


if __name__ == '__main__':
    dsn = pg.model_dump()
    table_name = 'views'
    total_rows = 100000
    batch = 10000

    with closing(psycopg2.connect(**dsn)) as conn, conn.cursor() as cursor:
        generator = DataGenerator()
        ps = PostgresStorage(conn, cursor, generator)
        res = ps.create_table(PSQL_CREATE_TABLE, table_name)
        print(res)

        res = ps.add(INSERT, table_name, total_rows, batch)
        print(metrics(res, 'insert', total_rows, batch))

        res = ps.read(SELECT, table_name)
        print(metrics(res, 'read', total_rows, batch))

        ps.drop_table(table_name)

    conn.close()
