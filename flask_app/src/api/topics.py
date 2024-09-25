from flask_restful import reqparse, abort, Resource

from src.services.metric import KafkaService
from src.schemas.topic import CreateTopic


def abort_if_topic_not_created(args):
    abort(
        400,
        message=f'The topic "{args["name"]}" was not created. '
        'Check the log file for more information'
    )


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help="Argument 'name' cannot be blank")
# parser.add_argument('partition', type=int, required=True, help="Argument 'partition' cannot be blank")
# parser.add_argument('retention', type=int, required=True, help="Argument 'retention' cannot be blank")
# parser.add_argument('min_replicas', type=int, required=True, help="Argument 'min_replicas' cannot be blank")
# parser.add_argument('replication', type=int, required=True, help="Argument 'replication' cannot be blank")


class Topic(Resource):
    """Endpoint to create Kafka topics."""

    def __init__(self, **kwargs) -> None:
        self.kafka_service: KafkaService = kwargs['kafka_service']

    def post(self):
        r"""Post method to create a Topic.

        Required arguments:
            name: string, name of topic.

        Default arguments:
            partition: integer, number of partitions.
            replication: integer, the replication factor determines the number
            of copies of each partition in Kafka.
            min_replicas: integer, defines the minimum number of replicas that
            must confirm the record.
            retention: integer, defines the period of time (in milliseconds)
            during which the data will be stored on the server.

        Returns:
            Response.

        Usage example with CURL:
            curl ^
            -X POST http://localhost:5000/api/create-topic ^
            -H "Content-Type: application/json" ^
            -d "{\"name\":\"<topic-name>\"}" ^
            -v
        """
        args = parser.parse_args()
        topic = CreateTopic(**args)
        created = self.kafka_service.create_topic(topic)
        if not created:
            abort_if_topic_not_created(args)
        return f"Topic '{args['name']}' was created", 201

    def delete(self):
        args = parser.parse_args()
        deleted = self.kafka_service.delete_topic(args['name'])
        return deleted
