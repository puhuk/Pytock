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
import numpy as np

stockCode = '083650' # 083650 비에이치아이



csv_data=csv.reader(file('Stock_list.csv'))
df=pd.read_csv('Stock_list.csv')
df.columns=['Company','Code']

conn=sqlite3.connect('test.db')
cursor=conn.cursor()
cursor.execute("Select Code from stock_info")
rows=cursor.fetchall()

trendOfInvestorUrl = 'http://finance.naver.com/item/frgn.nhn?code=' + stockCode
trendOfInvestorHtml = urlopen(trendOfInvestorUrl)
trendOfInvestorSource = BeautifulSoup(trendOfInvestorHtml.read(), "html.parser")

trendOfInvestorPageNavigation = trendOfInvestorSource.find_all("table", align="center")
trendOfInvestorMaxPageSection = trendOfInvestorPageNavigation[0].find_all("td", class_="pgRR")
trendOfInvestorMaxPageNum = int(trendOfInvestorMaxPageSection[0].a.get('href')[-3:])

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE if not exists trade(ID text UNIQUE, Code text, Stock text, Date text, Total text, InstitutionNetDeal text, ForeignNetDeal text, ForeignVol text, ForeignRate text);")

#for page in range(1, trendOfInvestorMaxPageNum + 1):
for a in range(1,len(rows)):
    stockCode=rows[a][0]
    print (stockCode)

    for page in range(1, 2):
        url = 'http://finance.naver.com/item/frgn.nhn?code=' + stockCode + '&page=' + str(page)
        html = urlopen(url)
        source = BeautifulSoup(html.read(), "html.parser")
        dataSection = source.find("table", summary="외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다.")
        dayDataList = dataSection.find_all("tr")

        # day: 날짜
        # institutionPureDealing: 기관순매매
        # foreignerPureDealing: 외인순매매
        # ownedVolumeByForeigner: 외인보유 주식수
        # ownedRateByForeigner : 외인 보유율

        for i in range(3, len(dayDataList)):
            if(len(dayDataList[i].find_all("td", class_="tc")) != 0 and len(dayDataList[i].find_all("td", class_="num")) != 0):

                day = dayDataList[i].find_all("td", class_="tc")[0].text
                total=dayDataList[i].find_all("td", class_="num")[3].text
                institutionPureDealing = dayDataList[i].find_all("td", class_="num")[4].text
                foreignerPureDealing = dayDataList[i].find_all("td", class_="num")[5].text
                try:
                    ownedVolumeByForeigner = dayDataList[i].find_all("td", class_="num")[6].text
                except:
                    ownedVolumeByForeigner=0
                try:
                    ownedRateByForeigner = dayDataList[i].find_all("td", class_="num")[7].text
                except:
                    ownedRateByForeigner=0

                #print "db start"
                print stockCode
                #print day
                #print total

                sql1 = "select Company from stock_info where code= ?"
                cursor.execute(sql1,(rows[a][0],))

                for row in cursor:
                    company=row[0]

                sql= "insert or replace into trade (ID, Code, Stock, Date, Total, InstitutionNetDeal, ForeignNetDeal, ForeignVol, ForeignRate) values (?,?,?,?,?,?,?,?,?);"
                cursor.execute(sql, (stockCode+day,stockCode,company,day, total,institutionPureDealing, foreignerPureDealing, ownedVolumeByForeigner, ownedRateByForeigner))


conn.commit()
conn.close()
