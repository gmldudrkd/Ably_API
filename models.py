from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class userInfo(db.Model):
    __tablename__ = 'userInfo'

    id = db.Column(db.String(50), primary_key=True)
    sub_id = db.Column(db.String(50))
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
