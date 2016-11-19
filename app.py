import os
import configparser

import pymysql

from flask import Flask, jsonify, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from database import db
from models.exams import Exam
from models.users import User
from modules.upload import save_data, allowed_file

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

        # TODO: check if phone number exists
        if User.query.filter_by(phone_number=phone_number).all():
            return jsonify(status='ERROR', error='Phone number exists!')

        # TODO: encrypt password.
        user = User(phone_number, password)
        user_id = db.session.add(user)
        db.session.commit()
        return jsonify(status='OK', user_id=user_id, error='')


@app.route('/alpha-api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user_info = request.json
        phone_number = user_info.get('phone_number')
        password = user_info.get('password')

        user = User.query.filter(User.phone_number == phone_number, User.password == password).first()
        if user is not None:
            return jsonify(status='OK', error='')
        else:
            return jsonify(status='ERROR', error='Phone number or password not correct.')


@app.route('/alpha-api/user/<uid>', methods=['PUT'])
def update_user_info(uid):
    user_info = request.json
    user = User.query.get(uid)
    user.phone_number = user_info.get('phone_number')
    user.password = user_info.get('password')
    user.age = user_info.get('age')
    user.gender = user_info.get('gender')
    db.session.commit()
    return jsonify(user.to_json())


@app.route('/alpha-api/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        uploaded_file = request.files['data']
        if uploaded_file and allowed_file(uploaded_file.filename):
            save_data(request.form.to_dict())

            filename = secure_filename(uploaded_file.filename)
            print(os.path.join(UPLOAD_FOLDER, filename))
            uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))

            print(jsonify(filename=filename))
            return jsonify(filename=filename)
        return jsonify(status='error'), 500
    # show upload page.
    exams = Exam.query.all()
    return render_template('upload.html', exams=exams)


@app.route('/alpha-api/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=7000)