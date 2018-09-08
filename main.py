# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 16:36:41 2018

@author: gaoha
"""
import json
import csv
import random
from play import play
from province import province
from key import key_generate
from attack import get_province
from create_map import create_map


def jsonGenerate(model):
    name = globals()
    rules, prov_dict = ruleGenerate()
    your_castle = ""
    computer_castle = []
    if model == 1:
        map1 = create_map(your_castle, computer_castle)
    prov = get_province()
    computer_choice = play(prov, your_castle, computer_castle, rules)
    computer_castle.append(computer_choice)
    list_computer_castle = name[computer_choice].birth
    list_computer_castle.sort()
    for i in list_computer_castle:
        computer_castle.append(prov_dict[str(i)])
    if model == 1:
        map2 = create_map(your_castle, computer_castle)
    key = key_generate(rules, your_castle, computer_castle)
    jsonObject = [{"rules": rules},
                  {"your_castle": your_castle, "computer_castle": computer_castle},
                  {"your_choice": "", "computer_choice": computer_choice},
                  {"key": key}]
    encodedjson = json.dumps(jsonObject)
    if model == 1:
        return encodedjson, map1, map2
    else:
        return encodedjson


def ruleGenerate():
    prov_dict = {}
    prov = []
    names = globals()
    filename = './static/information.csv'
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        m = 0
        for row in reader:
            if m == 0:
                m += 1
                continue
            prov.append(row[2])
            prov_dict[row[0]] = row[2]
            names[row[2]] = province(row[0], row[1], row[3], [], [])

    print(prov_dict)

    num_rules = random.randint(70, 150)
    rules = []
    m = 0
    repeat = []
    for i in range(num_rules):
        killer_id = random.randint(1, 34)
        killee_id = random.randint(1, 34)
        if killer_id == killee_id:
            continue
        if [killer_id, killee_id] in repeat:
            continue
        repeat.append([killer_id, killee_id])
        names[prov_dict[str(killer_id)]].sheng(killee_id)
        names[prov_dict[str(killee_id)]].kill(killer_id)
        m += 1
        rules.append([prov_dict[str(killer_id)], prov_dict[str(killee_id)]])
        # print("killer_id: %d ==> killee_id: %d " %(killer_id, killee_id))
        print(prov_dict[str(killer_id)], end='')
        print(" ==> ", end='')
        print(prov_dict[str(killee_id)])
    print(rules)
    # print("asdasdasdasdasd")
    # print("生成的规则数：", m)

    for i in prov:
        names[i].show()

    return rules, prov_dict
