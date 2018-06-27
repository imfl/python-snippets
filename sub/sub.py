# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 22:39:41 2018

@author: FL
"""

import subprocess
import sys


def pyMain(x):
    subprocess.Popen([sys.executable, 'te.py'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
    return x + 1024
