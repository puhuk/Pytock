# -*- coding: utf-8 -*-
#Python 2.7 버전 사용
import urllib
import time
#파싱 후 디비 삽입

from urllib2 import urlopen
from bs4 import BeautifulSoup
import sqlite3
import csv
import pandas as pd
import datetime, time
import numpy as np


csv_data=csv.reader(file('Stock_list.csv'))
df=pd.read_csv('Stock_list.csv')
df.columns=['Company','Code']

conn=sqlite3.connect('test.db')
cursor=conn.cursor()
cursor.execute("Select Code from stock_info")
rows=cursor.fetchall()


conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE if not exists Point(Stock text, Date text, Point float);")

print "중장투종목"
#for page in range(1, trendOfInvestorMaxPageNum + 1):
for a in range(1,len(rows)):
    stockCode=rows[a][0]
    cursor.execute("Select Company from stock_info where Code= :CP", {"CP":stockCode})

    rowa = cursor.fetchall()

    #print (stockCode)

    #stockCode="068270"

    url = 'http://finance.naver.com/item/main.nhn?code=' + stockCode
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    dataSection = source.find("table", summary="투자의견 정보")
    try:
        dayDataList = dataSection.find_all("tr")
    except:
        dayDataList=""


    #print stockCode
    try:
        if(float(dayDataList[0].find_all("span",class_="f_up")[0].text[0][:4])>=4.00):
            point="%0.2f" % float(dayDataList[0].find_all("span",class_="f_up")[0].text[:4])
            print rowa[0][0], dayDataList[0].find_all("span",class_="f_up")[0].text[:4], point
            sql = "insert or replace into Point (Stock, Date, Point) values (?,?,?);"
            cursor.execute(sql, (rowa[0][0], datetime.date.today(), point))
    except:
        stockCode=0


conn.commit()
conn.close()