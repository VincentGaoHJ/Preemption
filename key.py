# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 12:41:51 2018

@author: gaoha
"""


def key_generate(rules, your_castle, computer_castle):
    private_key = "6316316316"
    key_list = str(rules) + str(your_castle) + str(computer_castle) + private_key
    key = hash(key_list)
    return key


def key_check(rules, your_castle, computer_castle, key):
    keyCheck = key_generate(rules, your_castle, computer_castle)
    if keyCheck == key:
        print('Hash success')
        return True
    else:
        print('Hash failed')
        return False
