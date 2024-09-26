from flask import Blueprint
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token


bp = Blueprint('main', __name__)


@bp.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')


@bp.route('/login', methods=["POST"])
def login():
    r"""Endpoint for testing login and generate access token.

    Returns:
        Access token.

    Usage example with CURL:
        curl ^
        -X POST http://localhost:5000/login ^
        -H "Content-Type: application/json; charset=utf-8" ^
        -d "{\"username\":\"test\",\"password\":\"test\"}" ^
        -v
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({'msg': 'Bad username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
