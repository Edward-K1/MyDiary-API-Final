from functools import wraps
import jwt
from flask import request, jsonify, make_response
from . import create_app


def token_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return make_response(jsonify({"Error": "Token is missing"}), 403)

        try:
            app = create_app()  # We need that secret key

            data = jwt.decode(token, app.config['SECRET_KEY'])
            user_id = data['user_id']

        except:
            return make_response(jsonify({"Error": "Token is invalid"}), 403)

        return function(user_id, *args, **kwargs)

    return decorated
