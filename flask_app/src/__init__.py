import os

from flask import Flask
from pymongo import MongoClient

from .api.v1.topics import Topic
from .api.v1.messages import Message
from .services.metric import KafkaService
from .api.v1.likes import Like
from .api.v1.bookmarks import Bookmark
from .api.v1.reviews import Review
from .services.storage import MongoStorage
from .core.config import settings


def create_app(test_config=None):
    # Create and configure the app.
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, instance_path=basedir + '/core')
    app.config.from_mapping(
        SECRET_KEY=settings.secret_key,
        JWT_SECRET_KEY=settings.jwt_secret_key,
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

        # Page for testing
        @app.route('/hello')
        def hello():
            return 'Hello, World!'

    # Ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import main
    app.register_blueprint(main.bp)

    from flask_jwt_extended import JWTManager
    # Initialize a JWTManager with this flask application.
    jwt = JWTManager(app)

    from .api.v1 import app_api, api
    app.register_blueprint(app_api)

    kafka_service = KafkaService()
    api.add_resource(Topic, '/api/create-topic', resource_class_kwargs={'kafka_service': kafka_service})
    api.add_resource(Message, '/api/message', resource_class_kwargs={'kafka_service': kafka_service})
    
    client = MongoClient(settings.mongo_host, settings.mongo_port)
    mongo_storage = MongoStorage(client)
    api.add_resource(Like, '/api/like', resource_class_kwargs={'mongo_storage': mongo_storage})
    api.add_resource(Bookmark, '/api/bookmark', resource_class_kwargs={'mongo_storage': mongo_storage})
    api.add_resource(Review, '/api/review', resource_class_kwargs={'mongo_storage': mongo_storage})

    # Page for work testing
    @app.route('/working')
    def working():
        return 'Hello, Flask app is running!'
    return app

# RUN locally:
# cd flask_app
# flask --app src run --debug
