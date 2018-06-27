# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 22:43:34 2018

@author: FL
"""


import time

tt = open("tt.txt", "a")

for _ in range(5):
    tt.write("this time it will @ %s\n" % time.ctime(time.time()))
    time.sleep(2)

tt.write("--------------------------------------------------\n")

tt.close()
