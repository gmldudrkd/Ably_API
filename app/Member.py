from flask import request, jsonify
from flask_restful import Resource
import database
import re
from app.function import *

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

        # 회원가입
        result = database.create(request)
        if(result == "OK"):
            msg = "회원가입 완료"
            data = { 'id': id }
            result_data = return_set("TRUE", msg, data)
            return jsonify(result_data)