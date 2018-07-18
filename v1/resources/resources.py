from flask import jsonify, make_response
from flask_restful import Resource, request,reqparse
from ..models.models import User, DiaryEntry
from ..models.fields import user_fields, diary_entry_fields, user_fields_types, diary_entry_types
from ..api.Helpers import validate_and_assemble_data, assign_data
import sys


class UserResource(Resource):
    def get(self):
        return make_response(jsonify({"Users": User.get_all_users()}), 200)

    def post(self):
        data = request.get_json()
        result=validate_and_assemble_data(data,user_fields,user_fields_types)
        res_msg=result[2]
        success_msg="user registered successfully. " + res_msg

        if not result[0]:
            return make_response(jsonify({"status":"fail","message":res_msg}),400)

        _user=assign_data(User,result[1])

        _user.save()

        return make_response(jsonify({"status":"success","message":success_msg}),201)



class DiaryResource(Resource):
    def get(self):
        return make_response(
            jsonify({
                "Diary Entries": DiaryEntry.get_all_diary_entries()
            }), 200)

    def post(self):
        data=request.get_json()
        result=validate_and_assemble_data(data,diary_entry_fields,diary_entry_types)
        res_msg=result[2]
        success_msg= "new diary entry added"+res_msg

        if not result[0]:
            return make_response(jsonify({"status":"fail","message":res_msg}),400)

        entry=assign_data(DiaryEntry,result[1])
        entry.save()
        return make_response(jsonify({"status":"success","message":success_msg,"data":entry.json()}),201)


class DiaryEditResource(Resource):
    def get(self,entryId):
        print(entryId)
        f=open("test id.txt","w")
        f.write(str(entryId))
        f.close()



    def put(self):
        ...

    def delete(self):
        ...
