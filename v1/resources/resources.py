from flask import jsonify, make_response
from flask_restful import Resource, request
from ..models.models import User, DiaryEntry
from ..models.fields import user_fields, diary_entry_fields, user_fields_types, diary_entry_types
from ..api.Helpers import validate_and_assemble_data, assign_data


class UserResource(Resource):
    def get(self):
        return make_response(jsonify({"Users": User.get_all_users()}), 200)

    def post(self):
        data = request.get_json()
        result = validate_and_assemble_data(data, user_fields,
                                            user_fields_types)
        res_msg = result[2]
        success_msg = "user registered successfully. " + res_msg

        if not result[0]:
            return make_response(
                jsonify({
                    "status": "fail",
                    "message": res_msg
                }), 400)

        _user = assign_data(User, result[1])

        _user.save()

        return make_response(
            jsonify({
                "status": "success",
                "message": success_msg
            }), 201)


class DiaryResource(Resource):
    def get(self):
        return make_response(
            jsonify({
                "Diary Entries": DiaryEntry.get_all_diary_entries()
            }), 200)

    def post(self):
        data = request.get_json()
        result = validate_and_assemble_data(data, diary_entry_fields,
                                            diary_entry_types)
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
            return make_response(jsonify({"status": "fail","message": not_found_msg}),404)


        return make_response(jsonify({"Diary Entry": entry}), 200)


    def put(self, entryId):
        data = request.get_json()
        result = validate_and_assemble_data(data, diary_entry_fields,
                                            diary_entry_types)
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
            return make_response(jsonify({"status": "fail","message": not_found_msg}), 404)


        return make_response(jsonify({"status": "success","message": success_msg}), 201)



    def delete(self,entryId):
        entry=DiaryEntry.delete_entry(entryId)
        if entry:
            return make_response(jsonify({"status":"success","message":"entry deleted successfully"}),200)
        else:
            not_found_msg = f"entry with id:{entryId} not found"
            return make_response(jsonify({"status": "fail","message":not_found_msg}),404)

