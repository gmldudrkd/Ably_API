from flask import Flask
from flask_restful import Resource, Api

from app.Member import Member
from app.Join import Join
from app.UserInfo import Userinfo
from app.UserInfo import Userinfo2

app = Flask(__name__)
api = Api(app)

api.add_resource(Member,'/member')
api.add_resource(Join,'/join')
api.add_resource(Userinfo,'/info')
api.add_resource(Userinfo2,'/<int:id>')

@app.route('/')
def index():
    return "Hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)