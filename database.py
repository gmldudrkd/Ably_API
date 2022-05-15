import sqlite3 as sql
import models
from models import db
from flask import request


def create(request):
    conn = sql.connect("db.sqlite")
    cur = conn.cursor()

    id = request.json.get('id')
    sub_id = request.json.get('sub_id')
    password = request.json.get('password')
    email = request.json.get('email')
    phone_number = request.json.get('phone_number')

    cur.execute("INSERT INTO userInfo (id, sub_id, pwd, email, phone_number) VALUES (?,?,?,?,?)",
                (id, sub_id, password, email, phone_number))
    conn.commit()
    conn.close()
    return "OK"


def search(key, value, multi=None):
    conn = sql.connect("db.sqlite")
    cur = conn.cursor()

    where_field = ""
    if(multi == "Y"):
        for i in range(len(key)):
            if (i == 0):
                where_field += key[i] + "=? "
            else:
                where_field += "and " + key[i] + "=? "
        w_list = value
    else:
        where_field = key+"=?"
        w_list = (value,)

    cur.execute("select * from userInfo where "+where_field, w_list)
    rows = cur.fetchone();
    conn.close()

    return rows


def update(request):
    conn = sql.connect("db.sqlite")
    cur = conn.cursor()

    id = request.json.get('id')
    change_password = request.json.get('change_password')
    phone_number = request.json.get('phone_number')

    cur.execute("UPDATE userInfo SET pwd=? where id=? and phone_number=?", (change_password, id, phone_number))
    conn.commit()
    conn.close()

    return "OK"
