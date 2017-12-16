import requests, re
from bs4 import BeautifulSoup
import datetime

def naverRank(url):
	response = requests.get(url)
	if response.status_code == 200:
		html = response.text
		soup = BeautifulSoup(html, 'html.parser')
		cont = soup.select('#content > div.keyword_carousel > div > div > div')
		cont = re.sub('''<span class="title">''','\t',str(cont))
		cont = re.sub('''<ul class="rank_list">''','\t',str(cont))
		cont = re.sub('''<em class="num">''','\t',str(cont))
		cont = re.sub(r'<.*?>','',str(cont))
		cont = re.sub('\[','',str(cont))
		cont = re.sub('\]','',str(cont))
		cont = re.sub('\n','',str(cont))		
		cont = re.sub(', ','\n',str(cont))
		#', '기준으로 split?
		return(cont)
	else:
		return('err' + url)

def makeDate(start, end):
	startTime	= datetime.datetime.strptime(start.replace('T',' '), '%Y-%m-%d %H:%M:%S')
	endTime		= datetime.datetime.strptime(end.replace('T',' '), '%Y-%m-%d %H:%M:%S')
	endTime += datetime.timedelta(minutes=2)
	# h = int(start.split('T')[1].split(':')[0])
	# m = int(start.split('T')[1].split(':')[1])
	# if m % 2 == 1: m -= 1
	rst = list()
	while 1:
		# print(startTime)
		rst.append(str(startTime).replace(' ','T'))
		startTime += datetime.timedelta(minutes=2, seconds=30)
		if startTime > endTime: break
	return(rst)

if __name__ == '__main__':
	url = 'http://datalab.naver.com/keyword/realtimeList.naver?datetime='

	start	= '2017-08-31T00:00:00'
	end 	= '2017-09-30T00:00:00'
	dateList = makeDate(start,end)
	# print(dateList)

	for d in dateList:
		# print(naverRank(url + d))
		print(url + d)

	