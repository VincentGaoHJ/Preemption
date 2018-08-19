# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 18:20:51 2018

@author: gaoha
"""

class province :
    def __init__(self, name_id, name, area, birth, bekilled):
        self.name = name
        self.name_id = name_id
        self.area = area
        self.bekilled = bekilled
        self.birth = birth
        
    def sheng(self, killee_id):
        self.birth.append(killee_id)
        
    def kill(self, killer_id):
        self.bekilled.append(killer_id)
            
    def show(self):
        print(self.name_id, self.name, self.area, self.birth, self.bekilled)
        
print(province.__dict__)