# coding: utf8
import os
try:
    import configparser
except:
    from six.moves import configparser

import pymysql
import json
from OpenSSL import SSL
from flask import Flask, jsonify, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from database import db
from models.exams import Exam
from models.users import User
from modules.upload import save_data
from modules.api import register_user

UPLOAD_FOLDER = "uploads/"

app = Flask(__name__)

# load mysql config.
cf = configparser.ConfigParser()
cf.read('configs/dev.ini')
app.config['SQLALCHEMY_DATABASE_URI'] = cf.get('mysql', 'SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cf.getboolean('mysql', 'SQLALCHEMY_TRACK_MODIFICATIONS')

app.app_context().push()

db.init_app(app)
db.create_all()


# @app.errorhandler(Exception)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response
#

@app.before_first_request
def make_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)


@app.route('/alpha-api/')
def index():
    return jsonify(status='Flask is running!'), 200


@app.route('/alpha-api/register', methods=['POST'])
def register():
    if request.method == 'POST':
        user_info = request.json
        phone_number = user_info.get('phone_number')
        password = user_info.get('password')
        age = user_info.get('age')
        gender = user_info.get('gender')
        if User.query.filter_by(phone_number=phone_number).all():
            return jsonify(status='ERROR', error='电话号码已经注册')

        # TODO: encrypt password.
        user = User(phone_number, password, age, gender)
        db.session.add(user)
        db.session.flush()
        user.uuid = register_user(user.sync_info()).get("data")[0].get("uid")
        db.session.add(user)
        db.session.commit()

        return jsonify(status='OK', id=user.id, error='')


@app.route('/alpha-api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user_info = request.json
        phone_number = user_info.get('phone_number')
        password = user_info.get('password')

        user = User.query.filter(User.phone_number == phone_number, User.password == password).first()
        if user is not None:
            return jsonify(status='OK', error='', **user.to_dict())
        else:
            return jsonify(status='ERROR', error='用户名或密码不正确')


@app.route('/alpha-api/user/<uid>', methods=['GET', 'PUT'])
def update_user_info(uid):
    if request.method == 'PUT':
        user_info = request.json
        user = User.query.get(uid)
        user.phone_number = user_info.get('phone_number', user.phone_number)
        user.password = user_info.get('password', user.password)
        user.age = user_info.get('age', user.age)
        user.gender = user_info.get('gender', user.gender)
        db.session.commit()
        return jsonify(status='OK', error='', **user.to_dict())

    user = User.query.get(uid)
    return jsonify(status='OK', error='', **user.to_dict())


@app.route('/alpha-api/exam', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        print(request.form.to_dict())
        exam_info = json.loads(request.form.get('data'))
        filename = None
        if exam_info.get('file', None):
            uploaded_file = request.files['file']
            filename = secure_filename(uploaded_file.filename)
            exam_info['filename'] = filename
            uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
        err = None
        try:
            save_data(exam_info)
        except Exception as e:
            err = e.message
        if err:
            return jsonify(filename=filename, status='Error', error=err)
        return jsonify(filename=filename, status='OK', error=err)

    # show upload page.
    exams = Exam.query.all()
    return render_template('upload.html', exams=exams)


@app.route('/alpha-api/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
        db.session.remove()
    db.session.remove()

context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join(os.path.dirname(__file__), 'server.crt')
key = os.path.join(os.path.dirname(__file__), 'server.key')

if __name__ == '__main__':
    context = (cer, key)
    app.run(debug=True, port=7000, ssl_context=context, host='0.0.0.0', threaded=True)
