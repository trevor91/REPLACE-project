#검색어별로 등장 날짜 확인
import sys
import requests
import re
from bs4 import BeautifulSoup
import pymysql.cursors
from urllib.parse import quote
import csv
import os, subprocess
import pymysql

##### ##### ##### MAIN CODE ##### ##### ##### 

def getDate(key):
	url = "https://datalab.naver.com/keyword/realtimeSearch.naver?startDate=2017-03-29&endDate=2017-12-31&query="
	response = requests.get(url + key)
	if response.status_code == 200:
		html = response.text
		soup = BeautifulSoup(html, 'html.parser')
		tmp = soup.select('#wrap > script')[7].get_text().strip()
		tmp = re.sub("\$DATALAB\.SEARCH\_KEY\_LIST = ","",tmp)
		tmp = re.sub("\"","",tmp)
		tmp = re.sub(";","",tmp)
		tmp = re.sub("\[","",tmp)
		tmp = re.sub("\]","",tmp)
		tmp = tmp.split(',')

		if len(tmp) > minDateCnt:
			rst[key] = list()
			for s in tmp:
				# print(s.split('T')[0])
				rst[key].append(s)
	else:
		print('ERROR\t' + str(response.status_code) + '\n' + url)


def set_keyList():
	global keyList
	f = open(keyListFileName, 'r')
	rdr = csv.reader(f)
	for line in rdr:
		keyList.append(line[0])
	f.close()


def set_rst():
	for key in keyList:
		getDate(key)


def save_rst():
	keySort = sorted(rst, key=lambda k: len(rst[k]), reverse=True)
	with open(fileName, 'w') as f:
		for key in keySort:
			if len(rst[key]) != None:
				f.write("%s,%s\n"%(key,str(rst[key]).replace("[","").replace("]","").replace("\'","").replace(" ","")))


def dataConverterWithR():
	Rscript = "\"C:\\Program Files\\R\\R-3.4.1\\bin\\Rscript.exe\" \""
	src = os.getcwd() + "\\seqDate.R\" "
	arg = Rscript + src + fileName
	return(subprocess.call(arg))


def insertData():
	f = open(fileName, 'r')
	rdr = csv.reader(f)
	next(rdr) #ignore header
	for line in rdr:
		insertKeywordPeriod(line)
	f.close()


def insertKeywordPeriod(arg):
	try:
		with conn.cursor() as cursor:
			sql = 'INSERT IGNORE INTO tobigs.keyword_period (keyword, start, end) VALUES (%s, %s, %s)'
			cursor.execute(sql, (arg[0], arg[1], arg[2]))
		conn.commit()
	except Exception as e:
		print("DB INSERT ERROR " + e)
	

def removeFile():
	os.remove(fileName)

if __name__ == '__main__':
	global rst #결과 값을 저장하는 변수
	global keyList #keyword를 저장하는 변수
	global fileName
	global keyListFileName
	global minDateCnt #최소 n일 이상 검색되어야한다

	rst = dict()
	keyList = list()
	fileName = "day.csv"
	keyListFileName = "Data\\지진.csv"
	minDateCnt = 5

	# step1.
	set_keyList() 	#키워드 설정
	set_rst() 		#키워드를 기준으로 실검에 등장한 기간 크롤링
	save_rst() 	#csv파일로 저장

	# step2.
	Rstate = dataConverterWithR() #csv로 저장한 파일을 가공
	if Rstate == 1:
		print("R source Error")
		sys.exit()

	# step3.
	global conn
	host = sys.argv[1]
	user = sys.argv[2]
	pw = sys.argv[3]
	conn = pymysql.connect(host=host,user=user,password=pw,charset='utf8mb4')
	insertData() #csv파일을 DB에 저장
	removeFile() #csv파일 삭제