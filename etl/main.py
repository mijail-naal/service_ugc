import backoff

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaTimeoutError
from clickhouse_driver import Client

from utils.logger import logger
from utils.handler import backoff_hadler
from kafka_extractor import KafkaExtractor
from clickhouse_loader import ClickhouseLoader
from data_transformer import DataTransformer
from settings import kafka_settings as ks, settings
from queries import CREATE_EVENT_TABLE, EVENT_COLUMNS


@backoff.on_exception(backoff.expo, NoBrokersAvailable, on_backoff=backoff_hadler)
@backoff.on_exception(backoff.expo, KafkaTimeoutError, on_backoff=backoff_hadler)
def kafka_connection() -> KafkaConsumer:
    consumer = KafkaConsumer(
        ks.topics,
        bootstrap_servers=[ks.bootstrap_servers],
        auto_offset_reset=ks.auto_offset_reset,
        consumer_timeout_ms=ks.consumer_timeout_ms,
        group_id=ks.group_id,
        max_poll_records=ks.max_poll_records,
        enable_auto_commit=ks.enable_auto_commit
    )
    return consumer


if __name__ == '__main__':
    consumer = kafka_connection()
    kafka_extractor = KafkaExtractor(consumer)
    data_transformer = DataTransformer()

    batch = ks.max_poll_records
    total = kafka_extractor.last_registers(ks.topics, 2)

    times = total // batch + 1
    if total % batch == 0:
        times = total // batch

    res = data_transformer.record_to_string(times, kafka_extractor.run(batch))
    messages = data_transformer.generate_values(res)

    cluster = settings.cluster
    database = settings.database

    with Client(host=settings.clickhouse_host) as client:
        loader = ClickhouseLoader(client, cluster)
        res = loader.start(database, CREATE_EVENT_TABLE)
        logger.info(res)
        res = loader.load(database, settings.table, EVENT_COLUMNS, messages)
        logger.info(res)
        # loader.drop_table('kino.events')
        loader.close()

    kafka_extractor.stop()
    logger.info('Data added to Clickhouse')
