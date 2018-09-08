# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, Response
from chinaMap import baseMap
from main import jsonGenerate
from attack import attack

app = Flask(__name__)


# 游戏主界面
@app.route('/', methods=['GET'])
def hello_world():
    data = baseMap()
    return render_template("base.html", title=u"欢迎", data=data)


# 获取带有可视化界面的题目
@app.route('/register_image', methods=['GET'])
def register_image():
    # print(request.data)
    json, data, data1 = jsonGenerate(1)
    title = u"获取题目"
    return render_template("register.html", title=title, data=data, data1=data1, json=json)


# 获取没有可视化界面的题目
@app.route('/register', methods=['GET'])
def register():
    # print(request.data)
    encodedjson = jsonGenerate(0)
    title = u"获取题目"
    return Response(encodedjson, mimetype='application/json')


# 获取带有可视化的对战过程图以及电脑落子结果
@app.route('/play_image', methods=['POST'])
def play_image():
    # print(request.data)
    encodedjson, data, data1 = attack(request.data, 1)
    title = u"对战过程中"
    return render_template("register.html", title=title, data=data, data1=data1, json=encodedjson)


# 获取电脑落子结果
@app.route('/play', methods=['POST'])
def play():
    # print(request.data)
    encodedjson = attack(request.data, 0)
    title = u"对战过程中"
    return Response(encodedjson, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
