# -*- coding: utf-8 -*-
#Python 2.7 버전 사용
import urllib
import time
#디비에서 검색

from urllib2 import urlopen
from bs4 import BeautifulSoup

import sqlite3
import datetime

d=datetime.date.today()
year=str(d.year)

if(d.month)<10:
    month="0"+str(d.month)
else:
    month=str(d.month)
    
day=str(d.day)

today=year+"."+month+"."+day
date="2017.09.21"
print today

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
#cursor.execute("select * from trade where Date= :CP",{"CP":date})

cursor.execute("select * from trade where Code= :CP order by date DESC",{"CP":'083650'})

rows=cursor.fetchall()

print(rows)
print(rows[0][3])
print(str(rows[1][3]))

conn.commit()
conn.close()
