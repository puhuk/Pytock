# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup

url="http://finance.naver.com/item/main.nhn?code=065680"
soup = BeautifulSoup(urllib2.urlopen(url).read())
#pkg_list=soup.findAll("div", "first")
table=soup.find("div","first")
trs=table.find("tr","strong").findAll("td")

#시가총액

total_val=str(trs)[str(trs).find('m">')+3:str(trs).find('</em')].strip()+" "+str(trs)[str(trs).find('em>')+3:str(trs).find('</td')].strip()
print "시총 : " + total_val

#최근 연간 실적
table=soup.find("table","tb_type1 tb_num tb_type1_ifrs")
trs=table.tbody.tr.find("td","t_line cell_strong")

latest_yearly_sales=str(trs)[str(trs).find('g">')+3:str(trs).find('</td')].strip()
print "최근 연간 매출 : "+latest_yearly_sales+ " 억원"

#latest_yearly_profit



last_annual_performance = table



#
#count = 1
#for i in pkg_list:
#	title = i.findAll('a')
#	print count, "위: ", str(title)[str(title).find('title="')+7:str(title).find('">')]
#	count=count+1

