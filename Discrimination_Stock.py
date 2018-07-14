# -*- coding: utf-8 -*-

#Python 2.7 버전 사용
import urllib
import time


from urllib2 import urlopen
from bs4 import BeautifulSoup

#해당 종목의 거래량 급등 판별


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

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
#cursor.execute("select * from trade where Date= :CP",{"CP":date})

cursor.execute("select * from stock_info")

rowss=cursor.fetchall()

for i in range(1, len(rowss)):
#for i in range(1, 15):
        stock_code=rowss[i][1]
        cursor.execute("select Stock, Date, Total, InstitutionNetDeal, ForeignNetDeal from trade where Code= :CP order by date DESC",{"CP":stock_code})

        rows=cursor.fetchall()
        #print(i,stock,rows)

        sum=0
        stock= rows[0][0]

        for j in range(0,len(rows)):
            try:
                vol=int(rows[j][2].replace(',','').strip())
            except:
                vol=0
            sum = sum + vol
            cnt = j
            #print (i,stock,rows[i][0],rows[i][1],sum,cnt)

        average=sum/(cnt+1)

        try:
            vol = int(rows[0][2].replace(',', '').strip())
        except:
            vol = 0

        '''# 당일 거래량 평균 대비 10배 넘는 종목 검색'''

        if (average != 0):
            if (round(float(vol) / float(average) * 100.00, 2) > 1000):
                print "거래량 평균 대비 10배 이상 : ", stock

        # print ("=================================================")

        # 10거래일 중 5거래일 이상 기관 순매수 및 거래량 평소대비 5배 이상 증가 종목
        cnt=0
        for j in range(0, 10):
            try:
                if(rows[j][3][0]=='+'):
                    cnt=cnt+1
            except:
                cnt=0

        if (average!=0):
            if(cnt>=5 and round(float(vol)/float(average)*100.00,2)>700):
                print "5거래일 이상 기관 순매수 및 거래량 평소대비 10배 이상 증가 : ", stock

        # 10거래일 중 5거래일 이상 기관 순매수 및 거래량 평소대비 5배 이상 증가 종목
        cnt = 0
        for j in range(0, 25):
            try:
                if (rows[j][3][0] == '+'):
                    cnt = cnt + 1
            except:
                cnt = 0

        if (average != 0):
            if (cnt >= 24):
                print "25거래일 이상 기관 순매수 : ", stock

        # 기관, 외인 쌍끌이 종목
        ins_cnt = 0
        for_cnt = 0
        for j in range(0, 10):
            try:
                if (rows[j][3][0] == '+'):
                    ins_cnt = ins_cnt + 1
                if(rows[j][4][0]=='+'):
                    for_cnt=for_cnt+1
            except:
                ins_cnt = 0
                for_cnt=0

        if (average != 0):
            if (ins_cnt >= 8 and for_cnt>=8):
                print "기관/외인 쌍글이 : ", stock


