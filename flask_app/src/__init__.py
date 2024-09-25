import os

from flask import Flask

from .core.config import settings


def create_app(test_config=None):
    # Create and configure the app.
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, instance_path=basedir+'/core')
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

    from .api import app_api, api
    app.register_blueprint(app_api)

    from .api.topics import Topic
    from .api.messages import Message
    from .services.metric import KafkaService
    kafka_service = KafkaService()
    api.add_resource(Topic, '/api/create-topic',
                     resource_class_kwargs={'kafka_service': kafka_service})
    api.add_resource(Message, '/api/message',
                     resource_class_kwargs={'kafka_service': kafka_service})

    # Page for work testing
    @app.route('/working')
    def working():
        return 'Hello, Flask app is running!'
    return app

# RUN locally:
# cd flask_app
# flask --app src run --debug
