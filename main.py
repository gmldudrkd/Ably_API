from flask import request, jsonify
from flask_restful import Resource
import database
import json, requests
import re

class Member(Resource):
    # 회원가입
    def post(self):
        data = ""

        id = request.json.get('id')
        sub_id = request.json.get('sub_id')
        password = request.json.get('password')
        email = request.json.get('email')
        phone_number = request.json.get('phone_number')

        # 정보 유효성 처리
        if(id == "" or id == None
                or password == "" or password == None
                or email == "" or email == None
                or phone_number == "" or phone_number == None
                or sub_id == "" or sub_id == None):
            msg = "필수 값이 누락되었습니다."
            result_data = return_set("FALSE", msg, data)
            return jsonify(result_data)

        msg_list = []
        result = database.search('id',id)
        if (result != None):
            msg_list.append("중복된 아이디 입니다.[id : " + id + "]")

        result = database.search('sub_id',sub_id)
        if (result != None):
            msg_list.append("중복된 닉네임 입니다.[sub_id : " + sub_id + "]")

        text_compile = re.compile('[^A-Za-z0-9]')
        over_chk = text_compile.findall(id)
        if(len(over_chk) > 0):
            msg_list.append("아이디는 영문과 숫자만 입력 가능합니다.[id : " + id + "]")

        text_compile = re.compile('[^A-Za-z0-9-=+,#?:^$.@*※~&%ㆍ!]')
        over_chk = text_compile.findall(password)
        if (len(over_chk) > 0 or len(password) < 6):
            msg_list.append("비밀번호는 6자리 이상이며 지정된 특수문자 이외는 사용이 불가합니다.[password:" + password + "]")

        text_compile = re.compile('^[a-z,A-Z,0-9+-_.]+[@][a-zA-Z0-9-]+[\.][a-zA-Z0-9-.]+$')
        over_chk = text_compile.match(email)
        if (over_chk == None):
            msg_list.append("이메일 형식이 올바르지 않습니다.[email:" + email + "]")

        text_compile = re.compile('[^A-Za-z0-9-=+,#?:^$.@*※~&%ㆍ!]')
        over_chk = text_compile.findall(sub_id)
        if (len(over_chk) > 0):
            msg_list.append("닉네임은 지정된 특수문자 이외는 사용이 불가합니다.[sub_id:" + sub_id + "]")

        text_compile = re.compile('\d{3}-\d{3,4}-\d{4}')
        over_chk = text_compile.match(phone_number)
        if (over_chk == None):
            msg_list.append("전화번호 형식이 올바르지 않습니다.(형식:000-0000-0000)[phone_number:" + phone_number + "]")

        if(len(msg_list) >0):
            msg = "입력정보 유효성 오류"
            result_data = return_set("FALSE", msg, msg_list)
            return jsonify(result_data)

        # 번호인증,,?

        # 회원가입
        result = database.create(request)
        if(result == "OK"):
            msg = "회원가입 완료"
            data = { 'id': id }
            result_data = return_set("TRUE", msg, data)
            return jsonify(result_data)


class Join(Resource):
    # 로그인
    def post(self):
        data = ""
        id = request.json.get('id')
        result = database.search('id',id)
        if(result == None):
            msg = "아이디가 일치하지 않습니다."
            result_data = return_set("FALSE", msg, data)
            return jsonify(result_data)

        password = request.json.get('password')
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

        # 번호인증,,?

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


class Userinfo(Resource):
    # 내정보 보기
    def post(self):
        id = request.json.get('id')
        result = database.search('id',id)

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


def return_set(status,msg,data):
    return {'status': status,'msg': msg,'data': data }