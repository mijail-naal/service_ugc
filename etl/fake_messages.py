from random import choice, choices
from time import sleep

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

from settings import kafka_settings
from utils.logger import logger


admin = KafkaAdminClient(
    bootstrap_servers=[kafka_settings.bootstrap_servers]
)
new_topic = NewTopic(
    name=kafka_settings.topics,
    num_partitions=3,
    replication_factor=3,
    topic_configs={
        'min.insync.replicas': 2,
        'retention.ms': 86400000,
    }
)
try:
    admin.create_topics([new_topic])
except (TopicAlreadyExistsError) as e:
    logger.info(f'Topic already exists. Exception: {type(e).__name__}')
finally:
    admin.close()


producer = KafkaProducer(bootstrap_servers=[kafka_settings.bootstrap_servers])

users = ['user_123', 'user_125', 'user_127']
action = ['CLICK', 'VIEW', 'PAGE', 'CUSTOM']

rc = choices(users, k=10)

for user in rc:
    string = f'{choice(action)}-video catalogue section-00:53:24-00:53:24-00:53:25'

    producer.send(
        topic=kafka_settings.topics,
        value=f'{string}'.encode(),
        key=f'{user}'.encode(),
        partition=2
    )
    sleep(1)
    logger.info('sending a message')

logger.info('messages sent ...')
sleep(2)

producer.close()
