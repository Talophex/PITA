# -*- coding: utf-8 -*-
"""
Created on Fri Mar 08 09:38:27 2019

@author: Lucas
"""

import os
import time
os.rename('pita.db', 'pita-backup.db')
try:
    import CreateDatabase
except:
    print "error"
    time.sleep(5)