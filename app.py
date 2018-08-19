# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, Response
from chinaMap import baseMap
from werkzeug.utils import secure_filename
import json
import os
from main import jsonGenerate
from attack import attack

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def hello_world():
    data = baseMap()
    return render_template("base.html", title=u"欢迎", data=data)


@app.route('/register_image', methods=['GET', 'POST'])
def register_image():
    print(request.data)
    json, data = jsonGenerate(1)
    title = u"获取题目"
    return render_template("register.html", title=title, data=data, data1='', json=json)


@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.data)
    encodedjson = jsonGenerate(0)
    title = u"获取题目"
    return Response(encodedjson, mimetype='application/json')


@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['image01']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        return 'hello, ' + request.form.get('name', 'little apple') + '. success'
    else:
        return 'hello, ' + request.form.get('name', 'little apple') + '. failed'


@app.route('/play_image', methods=['POST'])
def play_image():
    print(request.data)
    encodedjson, data, data1 = attack(request.data, 1)
    title = u"对战过程中"
    return render_template("register.html", title=title, data=data, data1=data1, json=encodedjson)


@app.route('/play', methods=['POST'])
def play():
    print(request.data)
    encodedjson = attack(request.data, 0)
    title = u"对战过程中"
    return Response(encodedjson, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
