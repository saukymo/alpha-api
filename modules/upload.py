import time

from database import db
from models.exams import Exam
from models.users import User
# from app import app
from api import upload_data, upload_file

ALLOWED_EXTENSIONS = set(ext for ext in ['txt', "md", "mp4", "3gp"])

# db.init_app(app)

EXAM_CATEGORY = {
    "memory": 12000,
    "stand": 11000,
    "stride": 11000,
    "face": 13000,
    "sound": 14000,
    "tapping": 10000
}


def get_category_enum(exam_type):
    return EXAM_CATEGORY[exam_type]


def generate_exam_request_body(exam):
    if exam.exam_type in ["face", "sound"]:
        request_body = {
            "uid": get_register_uid(exam.user_uuid),
            "category": "%d" % get_category_enum(exam.exam_type),
            "fileType": "audio" if exam.exam_type == "sound" else "video"
            # "timestamp": time.strftime('%Y-%m-%d %H:%m:%S')
        }
    else:
        request_body = {
            "uid": get_register_uid(exam.user_uuid),
            "category": get_category_enum(exam.exam_type),
            "dataType": "scalar",
            "values": [{
                "value": exam.score,
                "timestamp": time.strftime('%Y-%m-%d %H:%m:%S')
            }]
        }

    return request_body


def get_register_uid(user_id):
    user = User.query.filter(User.id == user_id).first()
    return user.uuid


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_allowed_extensions():
    return ALLOWED_EXTENSIONS


def save_data(form):
    user_uuid = form.get('userId')
    filename = form.get('filename')
    created_time = form.get('createdTime')
    exam_type = form.get('examType')
    medicine = form.get('medicine')
    score = form.get('result')
    exam = Exam(user_uuid, filename, created_time, exam_type, medicine, score)

    if exam.exam_type in ["face", "sound"]:
        response = upload_file(generate_exam_request_body(exam), filename)
    else:
        response = upload_data(generate_exam_request_body(exam))
    exam.transaction_id = response.get("data")[0].get("tid")

    db.session.add(exam)
    db.session.commit()
