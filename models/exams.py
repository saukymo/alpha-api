# coding: utf8
from database import db


class Exam(db.Model):
    __table_args__ = ({"mysql_charset": "utf8mb4"})
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(40))
    filename = db.Column(db.String(40))
    created_time = db.Column(db.String(40))
    exam_type = db.Column(db.String(40))
    medicine = db.Column(db.Integer)

    def __init__(self, user_uuid, filename, created_time, exam_type, medicine):

        self.user_uuid = user_uuid
        self.filename = filename
        self.created_time = created_time
        self.exam_type = exam_type
        self.medicine = medicine

