""" This module handles requests passed to the various api endpoints """
from flask import jsonify, make_response
from flask_restful import Resource, request
import jwt
from .Helpers import validate_and_assemble_data, assign_data
from .security import token_required
from . import create_app
from .models.models import User, DiaryEntry
from .models.fields import (USER_FIELDS, DIARY_ENTRY_FIELDS, LOGIN_FIELDS,
                            USER_FIELDS_REGX, DIARY_FIELDS_REGX,
                            LOGIN_FIELDS_REGX, USER_FIELDS_HELP,
                            DIARY_ENTRIES_HELP, LOGIN_FIELDS_HELP)


class UserSignupResource(Resource):
    def post(self):
        data = request.get_json()
        result = validate_and_assemble_data(data, USER_FIELDS,
                                            USER_FIELDS_REGX, USER_FIELDS_HELP)
        res_msg = result[2]
        success_msg = "user registered successfully. " + str(res_msg)

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "failed",
                    "message": res_msg
                }), 400)

        _user = assign_data(User, result[1])

        result = _user.save()

        if result[1]:
            if result[1] == 409:
                return make_response(
                    jsonify({
                        "status": "failed",
                        "message": result[0]
                    }), 409)

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
        result = validate_and_assemble_data(
            data, LOGIN_FIELDS, LOGIN_FIELDS_REGX, LOGIN_FIELDS_HELP)
        res_msg = result[2]

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "failed",
                    "message": res_msg
                }), 400)

        login_result = User.get_login_user(result[1][0], result[1][1])

        if not login_result[0]:
            return make_response(
                jsonify({
                    "status": "failed",
                    "message": login_result[1]
                }), 401)

        user_id = login_result[0]

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
        data["user_id"] = user_id
        result = validate_and_assemble_data(
            data, DIARY_ENTRY_FIELDS, DIARY_FIELDS_REGX, DIARY_ENTRIES_HELP)

        res_msg = result[2]

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": res_msg
                }), 400)

        success_msg = "new diary entry added. " + str(res_msg)

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
        result = DiaryEntry.get_single_entry(entryId)

        if not result[0]:

            not_found_msg = f"entry with id:{entryId} not found"
            return make_response(
                jsonify({
                    "status": "failed",
                    "message": not_found_msg
                }), 404)

        return make_response(jsonify({"Diary Entry": result[0]}), 200)

    @token_required
    def put(user_id, self, entryId):
        data = request.get_json()
        data['user_id'] = user_id

        result = validate_and_assemble_data(
            data, DIARY_ENTRY_FIELDS, DIARY_FIELDS_REGX, DIARY_ENTRIES_HELP)

        res_msg = result[2]
        success_msg = f"diary entry modified successfully. " + str(res_msg)

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": res_msg
                }), 400)

        edit_result = DiaryEntry.modify_entry(entryId, result[1][1],
                                              result[1][2])
        print(edit_result)

        if not edit_result[0]:
            if edit_result[1] == 403:
                return make_response(
                    jsonify({
                        "status":
                        "failed",
                        "message":
                        "an entry can only be modified on the day it was created"
                    }), 403)

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
            }), 202)

    @token_required
    def delete(user_id, self, entryId):
        result = DiaryEntry.delete_entry(entryId)

        if not result[0]:

            not_found_msg = f"entry with id:{entryId} not found"
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": not_found_msg
                }), 404)

        return make_response(
            jsonify({
                "status": "success",
                "message": "entry deleted successfully"
            }), 200)


class NotificationsResource(Resource):
    @token_required
    def get(self):
        pass

    @token_required
    def post(self):
        pass

    @token_required
    def delete(user_id, self):
        pass
