import os
import configparser

import pymysql

from flask import Flask, jsonify, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from models.history import History
from models.user import User
from utils.dbhelper import DBHelper
from utils.upload import allowed_file, get_allowed_extensions

app = Flask(__name__)

# load config.
cf = configparser.ConfigParser()
cf.read('configs/dev.ini')

connect_string = {}
for option in cf.options('mysqld'):
    connect_string[option] = cf.get('mysqld', option)
connect_string['port'] = int(connect_string['port'])

# TODO: mkdir uploads.
UPLOAD_FOLDER = 'uploads'
database_helper = DBHelper()


@app.before_request
def prepare():
    database_helper.prepare_database()


@app.route('/alpha-api/')
def index():
    return jsonify(status='Flask is running!'), 200


@app.route('/alpha-api/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        file = request.files['data']
        # history_id = request.form['id']
        if file and allowed_file(file.filename):

            history = History(request.form.to_dict(), file.filename)
            history.insert()
            user = User(request.form.to_dict())
            user.insert()

            filename = secure_filename(file.filename)
            print(os.path.join(UPLOAD_FOLDER, filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            print(jsonify(filename=filename))
            return jsonify(filename=filename)
        return jsonify(status='error'), 500
    # show upload page.
    return render_template('upload.html', get_histories=get_histories)


def get_histories():
    return History.get_all_histories()


@app.route('/alpha-api/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, port=7000)
