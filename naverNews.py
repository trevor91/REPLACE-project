import requests, re
from bs4 import BeautifulSoup
import datetime
import time
from urllib.parse import quote


def getUrl(query, start, end):
	mainURL = "https://search.naver.com/search.naver?where=news&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&docid=&nso=so%3Ar%2Cp%3Afrom{start2}to{end2}%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0&query={query}&ds={start}&de={end}"
	if(start==end):
		end = end[0:-1] + str((int(end[-1]) + 1))

	url = mainURL.format(\
		query = quote(query)\
		,start = start\
		,end = end\
		,start2 = re.sub('.','',start)\
		,end2 = re.sub('.','',end))
	return(url)


def getNextPage(soup):
	try:
		cont = soup.select('#main_pack > div.paging > a.next')
		for href in cont:
			return(href.get('href'))
	except:
		return(None)


def getSingleNewsUrl(soup):
	rst = list()
	try:			
		cont = soup.select('#main_pack > div.news.mynews.section > ul > li > dl > dd > a')
		for a in cont:
			rst.append(a.get('href'))
		return(rst)
	except:
		return(None)


def getResource(url):
	rst = dict()

	response = requests.get(url)

	# status check
	if response.status_code == 200:
		html = response.text
		soup = BeautifulSoup(html, 'html.parser')
		
		rst['news'] = getSingleNewsUrl(soup)
		print(len(rst['news']))
		for news in rst['news']:
			newsUrl.append(news)
		
		rst["next"] = getNextPage(soup)
		return(rst["next"])

	# ERROR
	elif response.status_code == 403:
		print('getNextPage()\terr\t' + str(response.status_code) + '\n' + url)
		return(None)
	else:
		print('getNextPage()\terr\t' + str(response.status_code) + '\n' + url)
		return(None)


def getNewsInfo(url):
	response = requests.get(url)
	if response.status_code == 200:
		html = response.text
		soup = BeautifulSoup(html, 'html.parser')
		try:			
			# cont = soup.select('#articeBody')
			cont = soup.select('#articleTitle')
		except:
			cont = soup.select('#content > div.end_ct > div > h2')
		for title in cont:
			prigg
	else:
		print("ERR\t" + url)


if __name__ == '__main__':
	global newsUrl
	newsUrl = list()
	
	# 해당조건의 뉴스기사 URL 생성
	query	= '이찬오'
	start	= '2017.07.04'
	end 	= '2017.09.19'
	url = getUrl(query = query, start = start, end = end)
	
	while 1:
		# URL check
		if(url[0:6] != "https:"):
			url = "https:" + url

		# get single new url & next page url. => return (next page)
		url = getResource(url)

		if(url == None):
			break

	# get news cont & ...etc
	for news in newsUrl:
		# print("news:\t" + news)
		getNewsInfo(news)
		
		