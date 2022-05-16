from flask import request, jsonify
from flask_restful import Resource
import database
import re
from app.function import *

class Userinfo(Resource):
    # 내정보 보기
    def post(self):
        id = request.json.get('id')
        phone_number = request.json.get('phone_number')

        if (id == "" or id == None
                or phone_number == "" or phone_number == None):
            msg = "필수 값이 누락되었습니다."
            result_data = return_set("FALSE", msg, "")
            return jsonify(result_data)

        text_compile = re.compile('\d{3}-\d{3,4}-\d{4}')
        over_chk = text_compile.match(phone_number)
        if (over_chk == None):
            msg = "전화번호 형식이 올바르지 않습니다.(형식:000-0000-0000)[phone_number:" + phone_number + "]"
            data = {'phone_number': phone_number}
            result_data = return_set("FALSE", msg, "")
            return jsonify(result_data)

        result = database.search(('id', 'phone_number'), (id, phone_number), "Y")

        status = "TRUE"
        data = ""
        if(result != None):
            msg = "조회되었습니다."
            data = { 'id': result[0],
                     'sub_id': result[1],
                     'password': result[2],
                     'email': result[3],
                     'phone_number': result[4] }
        if (result == None):
            status = "FALSE"
            msg = "일치하는 사용자가 없습니다"

        result_data = return_set(status,msg,data)
        return jsonify(result_data)