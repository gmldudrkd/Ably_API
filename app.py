from flask import Flask
from flask_restful import Api
from main import Member
from main import Join
from main import Userinfo

import os
from models import db

app = Flask(__name__)
api = Api(app)

api.add_resource(Member,'/member')
api.add_resource(Join,'/join')
api.add_resource(Userinfo,'/info')

@app.route('/')
def index():
    return "Hello world"

# DB설정
basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.app = app
db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)