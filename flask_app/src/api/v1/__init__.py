from flask import Blueprint
from flask_restful import Api

app_api = Blueprint('api', __name__)
api = Api(app_api)

# from . import metrics
