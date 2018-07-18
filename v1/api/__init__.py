from flask import Flask, request, current_app
from flask_restful import Api, Resource
import json

API_URL = "/api/v1"


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisisatestsecretkey'

    api = Api(app, prefix=API_URL)

    from ..resources.resources import DiaryResource,DiaryEditResource,UserResource

    api.add_resource(DiaryResource, '/entry/')
    api.add_resource(DiaryEditResource,'/entry/<entryId>')
    api.add_resource(UserResource,'/user/')


    return app
