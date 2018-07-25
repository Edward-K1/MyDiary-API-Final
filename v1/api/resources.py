""" This module handles requests passed to the various api endpoints """
from flask import jsonify, make_response
from flask_restful import Resource, request
from .models.models import User, DiaryEntry
from .models.fields import USER_FIELDS, DIARY_ENTRY_FIELDS, USER_FIELDS_TYPES, DIARY_ENTRY_TYPES
from .Helpers import validate_and_assemble_data, assign_data


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

        user_id = _user.save()

        if not user_id:
            return make_response(
                jsonify({
                    "status": "failed",
                    "message": "a database error occured"
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

        user_id = User.get_login_user(str(data.get('email')), str(data.get('password')))


        if not user_id:
            return make_response(jsonify({"status":"failed","message":"invalid login credencials"}),403)




class DiaryResource(Resource):
    def get(self):
        return make_response(
            jsonify({
                "Diary Entries": DiaryEntry.get_all_diary_entries()
            }), 200)

    def post(self):
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
    def get(self, entryId):
        entry = DiaryEntry.get_single_entry(entryId)

        if not entry:
            not_found_msg = f"entry with id:{entryId} not found"
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": not_found_msg
                }), 404)

        return make_response(jsonify({"Diary Entry": entry}), 200)

    def put(self, entryId):
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

    def delete(self, entryId):
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
