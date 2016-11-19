# coding: utf8
from database import db


class User(db.Model):
    __table_args__ = ({"mysql_charset": "utf8mb4"})
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.Boolean)
    password = db.Column(db.String(40))

    def __init__(self, phone_number, password, age=None, gender=None):
        self.phone_number = phone_number
        self.password = password
        self.age = age
        self.gender = gender

    def to_json(self):
        return {"phone_number": self.phone_number,
                "password": self.password,
                "age": self.age,
                "gender": self.gender
                }

