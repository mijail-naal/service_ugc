from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from src.services.storage import MongoStorage
from src.schemas.bookmark import BookmarkData


def abort_if_not_sent():
    abort(
        400,
        msg='The information was not sent. '
        'Check the log file for more information'
    )


parser = reqparse.RequestParser()
parser.add_argument('url', type=str, required=True, help="Argument 'url' cannot be blank")


class Bookmark(Resource):
    r"""Endpoint to storage bookmarks.

    Required arguments:
        user_id: string, user id or name, obtained from access token.
        url: string, url of the page.

    Returns:
        Response: Message and status code.

    Usage example of the post method with CURL:
        curl ^
        -X POST http://localhost:5000/api/bookmark ^
        -H "Content-Type: application/json" ^
        -H "Authorization: Bearer <Access Token>" ^
        -d "{\"url\":\"<string>\"}" ^
        -v
    """

    def __init__(self, **kwargs) -> None:
        self.mongo_storage: MongoStorage = kwargs['mongo_storage']

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        condition = {'user_id': current_user}
        collection = self.mongo_storage.connect('UsersDB', 'bookmarks')
        bookmarks = self.mongo_storage.get(collection, condition)
        all_bookmarks = [BookmarkData(**bookmark).model_dump_json() for bookmark in bookmarks]
        if not all_bookmarks:
            abort(400, msg='No document found')
        return all_bookmarks, 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        condition = BookmarkData(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'bookmarks')
        bookmark_sent = self.mongo_storage.insert(collection, condition, args)
        if not bookmark_sent:
            abort_if_not_sent()
        return 'bookmark sent to db', 200

    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        args = parser.parse_args()
        args['user_id'] = current_user
        condition = BookmarkData(**args).model_dump()
        collection = self.mongo_storage.connect('UsersDB', 'bookmarks')
        bookmark_delited = self.mongo_storage.delete(collection, condition)
        if not bookmark_delited:
            abort_if_not_sent()
        return 'Like deleted', 200
