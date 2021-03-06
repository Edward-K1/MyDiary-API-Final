""" This file creates the flask app, initialises the api and adds resources to it """
from flask import Flask, request, render_template
from flask_restful import Api, Resource

API_URL = "/api/v1"


def create_app():
    """ This function creates the flask app and adds the api resources to it"""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisisatestsecretkey'

    api = Api(app, prefix=API_URL)

    @app.route('/', methods=['GET'])
    def home():
        """ Render HTML template with documentation reference """
        return render_template("index.html")

    from .resources import (DiaryResource, DiaryEditResource,
                            UserSignupResource, UserLoginResource,
                            NotificationsResource)

    api.add_resource(UserSignupResource, "/auth/signup", "/auth/signup/")
    api.add_resource(UserLoginResource, "/auth/login", "/auth/login/")

    api.add_resource(DiaryResource, '/entries', '/entries/')
    api.add_resource(DiaryEditResource, '/entries/<int:entryId>')
    api.add_resource(NotificationsResource, '/notifications',
                     '/notifications/')

    return app
