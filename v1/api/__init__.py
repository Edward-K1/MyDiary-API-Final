""" This file creates the flask app, initialises the api and adds resources to it """
from flask import Flask, request
from flask_restful import Api, Resource

API_URL = "/api/v1"


def create_app():
    """ This function creates the flask app and adds the api resources to it"""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisisatestsecretkey'

    api = Api(app, prefix=API_URL)

    from .resources import DiaryResource, DiaryEditResource, UserResource

    api.add_resource(DiaryResource, '/entry', '/entry/')
    api.add_resource(DiaryEditResource, '/entry/<int:entryId>')
    api.add_resource(UserResource, '/user', '/user/')

    return app
