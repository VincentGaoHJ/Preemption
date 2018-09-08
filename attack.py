# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 22:10:46 2018

@author: gaoha
"""
import json
import csv
from key import key_check, key_generate
from create_map import create_map
from play import play


def score(your_castle):
    prov_dic = {}
    final_score = 0
    filename = './static/information.csv'
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        m = 0
        for row in reader:
            if m == 0:
                m += 1
                continue
            prov_dic[row[2]] = row[3]

    for i in your_castle:
        final_score += float(prov_dic[i])
    final_score = final_score * 2 - 964.473
    return final_score


def json_Generate(rules, your_castle, computer_castle, computer_choice):
    key = key_generate(rules, your_castle, computer_castle)
    jsonObject = [{"rules": rules}, {"your_castle": your_castle, "computer_castle": computer_castle},
                  {"your_choice": "", "computer_choice": computer_choice}, {"key": key}]
    encodedjson = json.dumps(jsonObject)
    return encodedjson


def json_failed_Generate(rules, your_castle, computer_castle, your_choice, computer_choice, rt):
    key = rt
    jsonObject = [{"rules": rules}, {"your_castle": your_castle, "computer_castle": computer_castle},
                  {"your_choice": "", "computer_choice": computer_choice}, {"key": key}]
    encodedjson = json.dumps(jsonObject)
    return encodedjson


def get_province():
    prov = []
    filename = './static/information.csv'
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        m = 0
        for row in reader:
            if m == 0:
                m += 1
                continue
            prov.append(row[2])
    return prov


def check_gameover(your_castle, computer_castle):
    num = len(your_castle) + len(computer_castle)
    if num >= 34:
        return True
    else:
        return False


def reset_castle(rules, your_castle, computer_castle, choice, player):
    if player == "your":
        if your_castle == "":
            your_castle = []
            your_castle.append(choice)
        else:
            your_castle.append(choice)
        for i in rules:
            if i[0] == choice:
                if i[1] in your_castle:
                    continue
                else:
                    your_castle.append(i[1])
                    if i[1] in computer_castle:
                        computer_castle.remove(i[1])

    if player == "computer":
        computer_castle.append(choice)
        for i in rules:
            if i[0] == choice:
                if i[1] in computer_castle:
                    continue
                if i[1] in your_castle:
                    your_castle.remove(i[1])
                    computer_castle.append(i[1])
    return your_castle, computer_castle


def attack(encodedjson, model):
    json_file = json.loads(encodedjson)
    rules = json_file[0]['rules']
    your_castle = json_file[1]['your_castle']
    computer_castle = json_file[1]['computer_castle']
    your_choice = json_file[2]['your_choice']
    computer_choice = json_file[2]['computer_choice']
    key = json_file[3]['key']

    if key_check(rules, your_castle, computer_castle, key) != True:
        rt = "抱歉，密钥匹配失败，请重新尝试！"
        json_failed_Generate(rules, your_castle, computer_castle, your_choice, computer_choice, rt)
        return encodedjson
    if your_choice in your_castle:
        rt = "抱歉，您选择的城堡已经被己方占领，请重新尝试！"
        json_failed_Generate(rules, your_castle, computer_castle, your_choice, computer_choice, rt)
        return encodedjson
    if your_choice in computer_castle:
        rt = "抱歉，您选择的城堡已经被敌方占领，请重新尝试！"
        json_failed_Generate(rules, your_castle, computer_castle, your_choice, computer_choice, rt)
        return encodedjson

    prov = get_province()

    if your_choice not in prov:
        rt = "抱歉，您选择的城堡不在中国的省份内，请重新尝试！"
        json_failed_Generate(rules, your_castle, computer_castle, your_choice, computer_choice, rt)
        return encodedjson

    your_castle, computer_castle = reset_castle(rules, your_castle, computer_castle, your_choice, "your")
    print(your_castle, computer_castle)

    if model == 1:
        map1 = create_map(your_castle, computer_castle)

    if check_gameover(your_castle, computer_castle):
        final_score = score(your_castle)
        rt = "恭喜你，您的游戏结束了，最后得分是：%s" % (final_score)
        encodedjson = json_failed_Generate(rules, your_castle, computer_castle, your_choice, computer_choice, rt)
        if model == 1:
            map2 = ""
            return encodedjson, map1, map2
        elif model == 0:
            return encodedjson

    computer_choice = play(prov, your_castle, computer_castle, rules)

    your_castle, computer_castle = reset_castle(rules, your_castle, computer_castle, computer_choice, "computer")
    print(your_castle, computer_castle)
    if model == 1:
        map2 = create_map(your_castle, computer_castle)

    if check_gameover(your_castle, computer_castle):
        final_score = score(your_castle)
        rt = "恭喜你，您的游戏结束了，最后得分是：%s" % final_score
        encodedjson = json_failed_Generate(rules, your_castle, computer_castle, your_choice, computer_choice, rt)
        if model == 1:
            return encodedjson, map1, map2
        elif model == 0:
            return encodedjson

    encodedjson = json_Generate(rules, your_castle, computer_castle, computer_choice)

    if model == 1:
        return encodedjson, map1, map2

    else:
        return encodedjson
