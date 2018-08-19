# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 17:44:41 2018

@author: gaoha
"""

import requests
import json
import csv
import re

def get_province():
    prov = []
    filename = './static/information.csv'
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        m = 0
        for row in reader :
            if m == 0 :
                m += 1
                continue
            prov.append(row[2])
    return prov

def get_rules():
    r = requests.post("http://127.0.0.1:5000/register")
    encodedjson = json.dumps(r.json())
    json_file = json.loads(encodedjson)
    rules = json_file[0]['rules']
    your_castle = json_file[1]['your_castle']
    computer_castle = json_file[1]['computer_castle']
    key = json_file[3]['key']
    
    return rules, your_castle, computer_castle, key
    
    
def play(prov, your_castle, computer_castle):
    for i in prov:
        if i not in your_castle:
            if i not in computer_castle:
                return i
            
def json_Generate(rules, your_castle, computer_castle, your_choice, key):
    jsonObject = [{"rules":rules}, {"your_castle":your_castle, "computer_castle":computer_castle},{"your_choice":your_choice, "computer_choice":""}, {"key":key}]
    encodedjson = json.dumps(jsonObject)
    return encodedjson

def connect(json_file):
    rt = requests.post("http://127.0.0.1:5000/play", data = json_file)
    encodedjson = json.dumps(rt.json())
    json_file = json.loads(encodedjson)
    rules = json_file[0]['rules']
    your_castle = json_file[1]['your_castle']
    computer_castle = json_file[1]['computer_castle']
    key = json_file[3]['key']
    
    return rules, your_castle, computer_castle, key


    return rules

def main():
    i = 1
    n = 50
    score_total = 0
    while True:
        rules, your_castle, computer_castle, key = get_rules()
        prov = get_province()
        while True:
            your_choice = play(prov, your_castle, computer_castle)
            encodedjson = json_Generate(rules, your_castle, computer_castle, your_choice, key)
            rules, your_castle, computer_castle, key = connect(encodedjson)
            #print(key)
            if isinstance(key, int) == False:
                score = re.sub(r'[\u4E00-\u9FA5]', "", key)
                score = re.sub('，', "", score)
                score = re.sub('：', "", score)
                break
        i += 1
        score = float(score)
        score_total += score
        print(score_total)
        if i == n:
            break
        
    print(score_total/n)
    
    
    
main()