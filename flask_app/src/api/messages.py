from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from src.services.metric import KafkaService
from src.schemas.message import SendMessage


def abort_if_message_not_sent(args):
    abort(
        400,
        msg=f"The message to topic '{args['topic']}' was not sent. "
            "Check the log file for more information"
    )


parser = reqparse.RequestParser()
parser.add_argument('topic', type=str, required=True, help="Argument 'topic' cannot be blank")
# parser.add_argument('key', type=str, required=True, help="Argument 'key' cannot be blank")
parser.add_argument('value', type=str, required=True, help="Argument 'value' cannot be blank")


class Message(Resource):
    """Endpoint to send a message to Kafka."""

    def __init__(self, **kwargs) -> None:
        self.kafka_service: KafkaService = kwargs['kafka_service']

    @jwt_required()
    def post(self):
        """
        Required arguments:
            topic: string, name of topic.
            key: string, user id or name, obtained from access token.
            value: string, message containing information about the event.

        Usage example with CURL:
            curl ^
            -H "Authorization: Bearer <Access Token>" ^
            -H "Content-Type: application/json" ^
            -X POST http://localhost:5000/api/message -v ^
            -d "{\"topic\":\"<name>\",\"value\":\"<some_message>\"}"
        """

        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['key'] = current_user
        message = SendMessage(**args)
        message_sent = self.kafka_service.send_message(message)
        if not message_sent:
            abort_if_message_not_sent(args)
        return f"Message {args['key']} sent", 200
