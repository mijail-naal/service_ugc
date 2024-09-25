from kafka import KafkaConsumer
from kafka.structs import TopicPartition
from kafka.errors import NoBrokersAvailable, TopicAlreadyExistsError, \
                         InvalidTopicError, KafkaTimeoutError

from utils.logger import logger


class KafkaExtractor:
    """Consumer to extract the data from Kafka Topic."""

    def __init__(self, consumer: KafkaConsumer) -> None:
        self.consumer = consumer

    def run(self, batch):
        try:
            consumer_records = self.consumer.poll(batch)

            for _, values in consumer_records.items():
                for record in values:
                    yield record
            # return True
        except (NoBrokersAvailable, TopicAlreadyExistsError, InvalidTopicError) as error:
            match error:
                case NoBrokersAvailable():
                    logger.info(f'No connection available. Exception: {type(error).__name__}')
                case TopicAlreadyExistsError():
                    logger.info(f'Topic already exists. Exception: {type(error).__name__}')
                case InvalidTopicError():
                    logger.info(f'Topic name is invalid. Exception: {type(error).__name__}')
            return False
        except (NoBrokersAvailable, KafkaTimeoutError) as error:
            logger.info(f'Exception: {error}')
            return False

    def last_registers(self, topic: str, partition: int) -> int:
        tp = TopicPartition(topic=topic, partition=partition)
        offset_id = self.consumer.end_offsets([tp])
        return offset_id[tp]

    def stop(self) -> bool:
        self.consumer.close()
        return True
