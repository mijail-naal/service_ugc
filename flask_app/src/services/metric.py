from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import NoBrokersAvailable, TopicAlreadyExistsError, \
    InvalidTopicError, KafkaTimeoutError, UnknownTopicOrPartitionError

from src.utils.abstract import BaseBrokerService
from src.utils.logger import logger
from src.core.config import settings
from src.schemas.topic import CreateTopic
from src.schemas.message import SendMessage


class KafkaService(BaseBrokerService):
    def create_topic(self, topic: CreateTopic) -> bool:
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=[f'{settings.kafka_host}:{settings.kafka_port}']
            )
            new_topic = NewTopic(
                name=topic.name,
                num_partitions=topic.partition,
                replication_factor=topic.replication,
                topic_configs={
                    'min.insync.replicas': topic.min_replicas,
                    'retention.ms': topic.retention,
                })
            admin.create_topics([new_topic])
            admin.close()
            return True
        except (NoBrokersAvailable, TopicAlreadyExistsError, InvalidTopicError) as error:
            match error:
                case NoBrokersAvailable():
                    logger.info(f'No connection available. Exception: {type(error).__name__}')
                case TopicAlreadyExistsError():
                    logger.info(f'Topic already exists. Exception: {type(error).__name__}')
                case InvalidTopicError():
                    logger.info(f'Topic name is invalid. Exception: {type(error).__name__}')
            return False

    def send_message(self, message: SendMessage) -> bool:
        try:
            producer = KafkaProducer(
                bootstrap_servers=[f'{settings.kafka_host}:{settings.kafka_port}'],
            )
            if not message.topic or not message.value:
                return False
            producer.send(
                topic=message.topic,
                key=message.key.encode(),
                value=message.value.encode(),
                partition=2
            )
            producer.close()
            return True
        except (NoBrokersAvailable, KafkaTimeoutError, AssertionError) as error:
            logger.info(f'Exception: {error}')
            return False

    def delete_topic(self, topic: str) -> bool:
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=[f'{settings.kafka_host}:{settings.kafka_port}']
            )
            admin.delete_topics([topic])
            admin.close()
            return True
        except (NoBrokersAvailable, UnknownTopicOrPartitionError, InvalidTopicError) as error:
            match error:
                case NoBrokersAvailable():
                    logger.info(f'No connection available. Exception: {type(error).__name__}')
                case UnknownTopicOrPartitionError():
                    logger.info(f'No topic partition. Exception: {type(error).__name__}')
                case InvalidTopicError():
                    logger.info(f'Topic name is invalid. Exception: {type(error).__name__}')
            return False
