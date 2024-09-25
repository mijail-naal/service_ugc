import vertica_python

from contextlib import closing

from config.settings import vt
from vertica_vt.vertica_storage import VerticaStorage
from utils.queries import VERTICA_CREATE_TABLE, INSERT, SELECT
from utils.data_generator import DataGenerator


def metrics(res, action, rows, batch):
    result = f"""
    Vertica {action} results:

    Total rows               |Batch                     | Average per {action:<12} | Total execution time
    -------------------------|--------------------------|--------------------------|----------------------
    {rows:<24} | {batch:<24} | {res / rows:<24} | {res:<24}
    """
    return result


if __name__ == '__main__':
    conn_info = vt.model_dump()
    table_name = 'views'
    total_rows = 100000
    batch = 10000

    with closing(vertica_python.connect(**conn_info)) as conn, conn.cursor() as cursor:
        generator = DataGenerator()
        vs = VerticaStorage(conn, cursor, generator)
        res = vs.create_table(VERTICA_CREATE_TABLE, table_name)
        print(res)

        res = vs.add(INSERT, table_name, total_rows, batch)
        print(metrics(res, 'insert', total_rows, batch))

        res = vs.read(SELECT, table_name)
        print(metrics(res, 'read', total_rows, batch))

        vs.drop_table(table_name)

    conn.close()
