import requests, re
from bs4 import BeautifulSoup
import datetime
import time
from urllib.parse import quote

class keyword:
	def __init__(self, myKeyword, startTime, endTime):
		self.myKeyword = myKeyword
		self.start = startTime
		self.end = endTime

		self.newsUrl = list()
		self.news = list()
	
	def getKeyword(self):
		return(self.myKeyword)

	def getstartTime(self):
		return(self.start)

	def getendTime(self):
		return(self.end)

	def getNews(self):
		return(self.news)


	############################## crawling function ##############################
	def getUrl(self):
		mainURL = "https://search.naver.com/search.naver?where=news&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&docid=&nso=so%3Ar%2Cp%3Afrom{start2}to{end2}%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0&query={query}&ds={start}&de={end}"
		if(self.start==self.end):
			self.end = self.end[0:-1] + str((int(self.end[-1]) + 1))

		url = mainURL.format(\
			query = quote(self.myKeyword)\
			,start = self.start\
			,end = self.end\
			,start2 = re.sub('.','',self.start)\
			,end2 = re.sub('.','',self.end))
		return(url)

	def getNextPage(self, soup):
		try:
			cont = soup.select('#main_pack > div.paging > a.next')
			for href in cont:
				return(href.get('href'))
		except:
			return(None)


	def getSingleNewsUrl(self, soup):
		rst = list()
		try:			
			cont = soup.select('#main_pack > div.news.mynews.section > ul > li > dl > dd > a')
			for a in cont:
				rst.append(a.get('href'))
			return(rst)
		except Exception as e:
			return(None)


	# get new url list
	def getResource(self, url):
		rst = dict()
		response = requests.get(url)
		# status check
		if response.status_code == 200:
			html = response.text
			soup = BeautifulSoup(html, 'html.parser')
			
			rst['news'] = self.getSingleNewsUrl(soup)
			print(len(rst['news']))
			for news in rst['news']:
				self.newsUrl.append(news)
			
			rst["next"] = self.getNextPage(soup)
			return(rst["next"])

		# ERROR
		elif response.status_code == 403:
			print('getNextPage()\terr\t' + str(response.status_code) + '\n' + url)
			time.sleep(10)
			self.getResource(url)
			return(None)
		else:
			print('getNextPage()\terr\t' + str(response.status_code) + '\n' + url)
			return(None)


	# news crawling
	def form1(self, url, soup): #http://news.naver.com # no redirect
		rst = dict()
		rst['url'] = url
		# get title
		rst['title'] = soup.select('#articleTitle')[0].text
		# get date
		rst['date'] = soup.select('#main_content > div.article_header > div.article_info > div.sponsor > span.t11')[0].text
		# get company name
		rst['company'] = soup.select('#main_content > div.article_header > div.press_logo > a > img')[0].get('title')
		# get contents
		rst['cont'] = soup.select('#articleBodyContents')[0].text
		return(rst)


	def form2(self, url, soup): # http://entertain.naver.com # redirect
		rst = dict()
		rst['url'] = url
		# get title
		rst['title'] = soup.select('#content > div.end_ct > div > h2')[0].text
		# get date
		rst['date'] = soup.select('#content > div.end_ct > div > div.article_info > span > em')[0].text
		# get company name
		rst['company'] = soup.select('#content > div.end_ct > div > div.press_logo > a > img')[0].get('alt')
		# get contents
		rst['cont'] = soup.select('#articeBody')[0].text
		return(rst)


	def getNewsInfo(self, url):
		response = requests.get(url, allow_redirects=True)
		# print(response.history) # redirect check.
		print(response.url)
		html = response.text
		soup = BeautifulSoup(html, 'html.parser')

		if response.status_code == 200:
			#http://news.naver.com
			if 'http://news.naver.com' in response.url:
				return(self.form1(url, soup))

			# http://entertain.naver.com
			elif 'http://entertain.naver.com' in response.url:
				return(self.form2(url, soup))
		else:
			print("getNewsInfo ERROR\t" + str(response.status_code) + '\t' + url)


	def newsCrawling(self):
		# step1. 해당조건의 뉴스기사 검색 URL 생성
		url = self.getUrl()

		# step2. 뉴스 기사 검색을 통해서 기사 URL list 생성
		while 1:
			# URL check
			if(url[0:6] != "https:"):
				url = "https:" + url

			# get single new url & next page url. => return (next page)
			url = self.getResource(url)
			if(url == None):
				break

		# step3. URL list에서 뉴스 기사 수집
		for news in self.newsUrl:
			print("news:\t" + news)
			self.news.append(self.getNewsInfo(news))


	############################## search function ##############################
	def removeWhiteSpace(self, string):
		pattern = re.compile(r'\s+')
		return(re.sub(pattern, '', string))


	def searchKeyword(self, *strings):
		newsTitle = list()
		newsCont = list()
		keywordList = list()

		# 공백 제거 (제목, 내용)
		for oneNews in self.news:
			newsTitle.append(self.removeWhiteSpace(oneNews['title']))
			newsCont.append(self.removeWhiteSpace(oneNews['cont']))

		# 공백 제거 (string)
		for string in strings:
			keywordList.append(self.removeWhiteSpace(string))


		# keywordList을 긴거 순으로 정렬
		keywordList.sort(key = len, reverse = True)

		
		# 검색
		for string in keywordList:
			for idx, title in enumerate(newsTitle):
				print('%s title count: %d' % (string, title.count(string)))
				newsTitle[idx] = re.sub(string, '', title)
			for idx, content in enumerate(newsCont):
				print('%s content count: %d' % (string, content.count(string)))
				newsCont[idx] = re.sub(string, '', content)
