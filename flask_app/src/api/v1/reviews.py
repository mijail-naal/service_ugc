from http import HTTPStatus

from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from src.services.storage import MongoStorage
from src.schemas.review import ReviewData, ReviewCondition, ReviewUpdate


def abort_if_not_sent():
    abort(
        HTTPStatus.BAD_REQUEST,
        msg='The information was not sent. '
        'Check the log file for more information'
    )


parser = reqparse.RequestParser()
parser.add_argument('film_id', type=str, required=True, help="Argument 'film_id' cannot be blank")
parser.add_argument('created_at', type=str, required=True, help="Argument 'created_at' cannot be blank")
parser.add_argument('user_review', type=str, required=True, help="Argument 'user_review' cannot be blank")


class Review(Resource):
    r"""Endpoint to interact with user review.

    Required arguments:
        film_id: string, id of film.
        user_id: string, user id or name, obtained from access token.
        created_at: datetime, date and time the review was created.
        user_review: string, text added by the user.

    Returns:
        Response: Message and status code.

    Usage example of the post method with CURL:
        curl ^
        -X POST http://localhost:5000/api/review ^
        -H "Content-Type: application/json" ^
        -H "Authorization: Bearer <Access Token>" ^
        -d "{\"film_id\":\"<uuid>\",\"created_at\":\"<datetime>\",\"user_review\":\"<text>\"}" ^
        -v
    """

    def __init__(self, **kwargs) -> None:
        self.mongo_storage: MongoStorage = kwargs['mongo_storage']

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        condition = ReviewCondition(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'reviews')
        review_doc = self.mongo_storage.get(collection, condition)
        if not review_doc:
            abort(HTTPStatus.BAD_REQUEST, msg='No document found')
        user_review = ReviewData(**review_doc[0]).model_dump()
        return user_review, HTTPStatus.OK

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        data = ReviewData(**args).model_dump()
        condition = ReviewCondition(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'reviews')
        review_sent = self.mongo_storage.insert(collection, condition, data)
        if not review_sent:
            abort_if_not_sent()
        return 'Review sent to db', HTTPStatus.OK

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        condition = ReviewCondition(**args).model_dump()
        new_data = ReviewUpdate(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'reviews')
        review_updated = self.mongo_storage.update(collection, condition, new_data)
        if not review_updated:
            abort_if_not_sent()
        return 'Review updated', HTTPStatus.OK

    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        condition = ReviewCondition(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'reviews')
        review_delited = self.mongo_storage.delete(collection, condition)
        if not review_delited:
            abort_if_not_sent()
        return 'Review deleted', HTTPStatus.OK
