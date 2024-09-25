from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from src.services.storage import MongoStorage
from src.schemas.like import LikeData, LikeCondition, LikeUpdate


def abort_if_not_sent():
    abort(
        400,
        msg='The information was not sent. '
        'Check the log file for more information'
    )


parser = reqparse.RequestParser()
parser.add_argument('film_id', type=str, required=True, help="Argument 'film_id' cannot be blank")
parser.add_argument('like', type=str, required=True, help="Argument 'like' cannot be blank")


class Like(Resource):
    r"""Endpoint to interact with user likes.

    Required arguments:
        film_id: string, id of film.
        user_id: string, user id or name, obtained from access token.
        Like: Bool, film like action.

    Returns:
        Response: Message and status code.

    Usage example of the post method with CURL:
        curl ^
        -X POST http://localhost:5000/api/like ^
        -H "Content-Type: application/json" ^
        -H "Authorization: Bearer <Access Token>" ^
        -d "{\"film_id\":\"<uuid>\",\"like\":\"<bool>\"}" ^
        -v
    """

    def __init__(self, **kwargs) -> None:
        self.mongo_storage: MongoStorage = kwargs['mongo_storage']

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        condition = LikeCondition(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'likes')
        like_doc = self.mongo_storage.get(collection, condition)

        if not like_doc:
            abort(400, msg='No document found')
        return like_doc[0]['like'], 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        data = LikeData(**args).model_dump()
        condition = LikeCondition(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'likes')
        like_sent = self.mongo_storage.insert(collection, condition, data)
        if not like_sent:
            abort_if_not_sent()
        return 'Like sent to db', 200

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        condition = LikeCondition(**args).model_dump()
        new_data = LikeUpdate(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'likes')
        like_updated = self.mongo_storage.update(collection, condition, new_data)
        if not like_updated:
            abort_if_not_sent()
        return 'Like updated', 200

    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        condition = LikeCondition(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'likes')
        like_delited = self.mongo_storage.delete(collection, condition)
        if not like_delited:
            abort_if_not_sent()
        return 'Like deleted', 200
