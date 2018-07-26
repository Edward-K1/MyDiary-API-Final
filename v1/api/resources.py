""" This module handles requests passed to the various api endpoints """
from flask import jsonify, make_response
from flask_restful import Resource, request
from .models.models import User, DiaryEntry
from .models.fields import USER_FIELDS, DIARY_ENTRY_FIELDS, USER_FIELDS_TYPES, DIARY_ENTRY_TYPES
from .Helpers import validate_and_assemble_data, assign_data
from .security import token_required
from . import create_app
import jwt


class UserSignupResource(Resource):
    def post(self):
        data = request.get_json()
        result = validate_and_assemble_data(data, USER_FIELDS,
                                            USER_FIELDS_TYPES)
        res_msg = result[2]
        success_msg = "user registered successfully. " + res_msg

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "failed",
                    "message": res_msg
                }), 400)

        _user = assign_data(User, result[1])

        result = _user.save()

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "failed",
                    "message": result[1]
                }), 500)

        return make_response(
            jsonify({
                "status": "success",
                "message": success_msg
            }), 201)


class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not "email" or not "password" in data:
            return make_response(
                jsonify({
                    "message": "email and password required"
                }), 400)

        if str(data.get("email")).strip() == '' or str(
                data.get("password")).strip() == '':
            return make_response(
                jsonify({
                    "message": "email and password required"
                }), 400)

        result = User.get_login_user(
            str(data.get('email')), str(data.get('password')))

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "failed",
                    "message": result[1]
                }), 401)

        user_id = result[0]
        app = create_app()  #leverage app instance to get secret key
        encoded_token = jwt.encode({
            "user_id": user_id
        }, app.config['SECRET_KEY'])

        return make_response(
            jsonify({
                "message":
                "Logged in successfully. Take note of your access-token. You'll need it to authenticate your requests",
                "access-token":
                encoded_token.decode('UTF-8')
            }), 200)


class DiaryResource(Resource):
    @token_required
    def get(user_id, self):
        return make_response(
            jsonify({
                "Diary Entries": DiaryEntry.get_all_diary_entries(user_id)
            }), 200)

    @token_required
    def post(user_id, self):
        data = request.get_json()
        result = validate_and_assemble_data(data, DIARY_ENTRY_FIELDS,
                                            DIARY_ENTRY_TYPES)
        res_msg = result[2]
        success_msg = "new diary entry added. " + res_msg

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": res_msg
                }), 400)

        entry = assign_data(DiaryEntry, result[1])
        entry.save()
        return make_response(
            jsonify({
                "status": "success",
                "message": success_msg
            }), 201)


class DiaryEditResource(Resource):
    @token_required
    def get(user_id, self, entryId):
        entry = DiaryEntry.get_single_entry(entryId)

        if not entry:
            not_found_msg = f"entry with id:{entryId} not found"
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": not_found_msg
                }), 404)

        return make_response(jsonify({"Diary Entry": entry}), 200)

    @token_required
    def put(user_id, self, entryId):
        data = request.get_json()
        result = validate_and_assemble_data(data, DIARY_ENTRY_FIELDS,
                                            DIARY_ENTRY_TYPES)
        res_msg = result[2]
        success_msg = f"diary entry with eid:{entryId} modified successfully. " + res_msg

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": res_msg
                }), 400)

        entry = DiaryEntry.modify_entry(entryId, result[1][0], result[1][1])
        if not entry:
            not_found_msg = f"entry with id:{entryId} not found"
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": not_found_msg
                }), 404)

        return make_response(
            jsonify({
                "status": "success",
                "message": success_msg
            }), 201)

    @token_required
    def delete(user_id, self, entryId):
        entry = DiaryEntry.delete_entry(entryId)
        if entry:
            return make_response(
                jsonify({
                    "status": "success",
                    "message": "entry deleted successfully"
                }), 200)
        else:
            not_found_msg = f"entry with id:{entryId} not found"
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": not_found_msg
                }), 404)
