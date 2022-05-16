from flask import request, jsonify
from flask_restful import Resource
import database
import re
from app.function import *

class Join(Resource):
    # 로그인
    def post(self):
        data = ""
        id = request.json.get('id')
        password = request.json.get('password')

        if (id == "" or id == None
                or password == "" or password == None):
            msg = "필수 값이 누락되었습니다."
            result_data = return_set("FALSE", msg, "")
            return jsonify(result_data)

        result = database.search('id',id)
        if(result == None):
            msg = "아이디가 일치하지 않습니다."
            result_data = return_set("FALSE", msg, data)
            return jsonify(result_data)

        result = database.search(('id', 'pwd'), (id, password), "Y")
        if (result == None):
            msg = "비밀번호가 일치하지 않습니다."
            result_data = return_set("FALSE", msg, data)
            return jsonify(result_data)

        msg = "로그인 성공"
        data = {'id': result[0], 'sub_id': result[1]}
        result_data = return_set("TRUE", msg, data)

        print(result_data)
        return jsonify(result_data)

    # 비밀번호 재설정
    def put(self):
        data = ""
        id = request.json.get('id')
        change_password = request.json.get('change_password')
        phone_number = request.json.get('phone_number')

        if (id == "" or id == None
                or change_password == "" or change_password == None
                or phone_number == "" or phone_number == None):
            msg = "필수 값이 누락되었습니다."
            result_data = return_set("FALSE", msg, "")
            return jsonify(result_data)

        text_compile = re.compile('\d{3}-\d{3,4}-\d{4}')
        over_chk = text_compile.match(phone_number)
        if (over_chk == None):
            msg = "전화번호 형식이 올바르지 않습니다.(형식:000-0000-0000)[phone_number:" + phone_number + "]"
            result_data = return_set("FALSE", msg, data)
            return jsonify(result_data)

        result = database.search(('id', 'phone_number'), (id, phone_number), "Y")
        if (result == None):
            msg = "존재하지 않는 아이디와 번호입니다."
            data = {'id': id, 'phone_number': phone_number}
            result_data = return_set("FALSE", msg, data)
            return jsonify(result_data)

        if(result[2] == change_password):
            msg = "이전과 동일한 비밀번호 입니다."
            data = {'id': id, 'change_password': change_password}
            result_data = return_set("FALSE", msg, data)
            return jsonify(result_data)

        database.update(request)
        msg = "비밀번호 재설정 완료"
        data = {'id': id, 'change_password': change_password}
        result_data = return_set("TRUE", msg, data)
        return jsonify(result_data)