import clickhouse_driver

from clickhouse_ch.clickhouse_storage import ClickhouseStorage
from utils.queries import CLICKHOUSE_CREATE_TABLE, INSERT, SELECT
from utils.data_generator import DataGenerator


def metrics(res, action, rows, batch):
    result = f"""
    Clickhouse {action} results:

    Total rows               |Batch                     | Average per {action:<12} | Total execution time
    -------------------------|--------------------------|--------------------------|----------------------
    {rows:<24} | {batch:<24} | {res / rows:<24} | {res:<24}
    """
    return result


if __name__ == '__main__':
    table_name = 'views'
    total_rows = 100000
    batch = 10000

    with clickhouse_driver.Client(host='localhost') as client:
        generator = DataGenerator()
        ch = ClickhouseStorage(client, generator)
        res = ch.create_table(CLICKHOUSE_CREATE_TABLE, table_name)
        print(res)

        res = ch.add(INSERT, table_name, total_rows, batch)
        print(metrics(res, 'insert', total_rows, batch))

        res = ch.read(SELECT, table_name)
        print(metrics(res, 'read', total_rows, batch))

        ch.drop_table(table_name)

        ch.close()
