from database import db
from models.exams import Exam
from models.users import User

ALLOWED_EXTENSIONS = set(ext for ext in ['txt', "md", "mp4", "3gp"])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_allowed_extensions():
    return ALLOWED_EXTENSIONS


def save_data(form):
    user_uuid = form.get('userId')
    filename = form.get('file')
    created_time = form.get('createdTime')
    exam_type = form.get('examType')
    medicine = form.get('medicine')
    exam = Exam(user_uuid, filename, created_time, exam_type, medicine)

    # phone_number = form.get('phone_number')
    # age = form.get('age')
    # gender = form.get('gender')
    # uuid = form.get('uuid')
    # user = User(phone_number, age, gender, uuid)

    db.session.add(exam)
    # db.session.add(user)
    db.session.commit()
