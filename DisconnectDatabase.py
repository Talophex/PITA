# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 09:38:27 2019

@author: Lucas
"""

import os
import time
from datetime import date
disconfilename = str(date.today())+'.db'
os.rename('pita.db', disconfilename)
try:
    import CreateDatabase
except:
    print "error"
    time.sleep(5)
os.system("rclone move "+disconfilename+" jrp-box:pita/")
