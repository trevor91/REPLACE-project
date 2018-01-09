#-*- coding:utf-8 -*-
import requests, re
from bs4 import BeautifulSoup
import datetime
import time
from urllib.parse import quote
import pymysql.cursors

class keyword:
    def __init__(self, keyword = None, startTime = None, endTime = None):
        self.myKeyword = keyword
        self.start = startTime
        self.end = endTime

        self.newsUrl = list()
        self.news = list()
        self.conn = 0

    def getKeyword(self):
        return(self.myKeyword)

    def getstartTime(self):
        return(self.start)

    def getendTime(self):
        return(self.end)

    def getNews(self):
        return(self.news)

    def setKeyword(self, keyword):
        self.myKeyword = keyword

    def setStart(self, start):
        self.start = start

    def setEnd(self, end):
        self.end = end


    ############################## crawling function ##############################
    def getUrl(self):
        mainURL = "https://search.naver.com/search.naver?where=news&ie=utf8&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&docid=&nso=so%3Ar%2Cp%3Afrom{start2}to{end2}%2Ca%3Aall&mynews=0&mson=0&refresh_start=0&related=0&query={query}&ds={start}&de={end}"

        # if(self.start==self.end):
        # 	self.end = self.end[0:-1] + str((int(self.end[-1]) + 1))

        url = mainURL.format(\
            query = quote(self.myKeyword)\
            ,start = self.start\
            ,end = self.end\
            ,start2 = re.sub('\.','',self.start)\
            ,end2 = re.sub('\.','',self.end))
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

            for single in rst['news']:
                self.insertNewsList(single)

            for news in rst['news']:
                self.newsUrl.append(news)

            rst["next"] = self.getNextPage(soup)
            return(rst["next"])

        # ERROR
        elif response.status_code == 403:
            print('getNextPage()\terr\t' + str(response.status_code) + '\n' + url)
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
        temp = "// flash 오류를 우회하기 위한 함수 추가"
        temp2 = "function _flash_removeCallback\(\) \{\}"
        if temp in rst['cont']:
            rst['cont'] = re.sub(temp, '', rst['cont'])
            rst['cont'] = re.sub(temp2, '', rst['cont'])
            rst['cont'] = re.sub('\n\n', '\n', rst['cont'])
        return(rst)


    def form2(self, url, soup): # http://entertain.naver.com # redirect
        rst = dict()
        rst['url'] = url
        # get title
        rst['title'] = soup.select('#content > div.end_ct > div > h2')[0].text
        # get date
        rst['date'] = soup.select('#content > div.end_ct > div > div.article_info > span > em')[0].text
        if '오전' in rst['date']:
            rst['date'] = re.sub('오전','',rst['date'])
        if '오후' in rst['date']:
            temp = rst['date'].split('오후')
            temp2 = temp[1].split(':')
            t = int(temp2[0]) + 12
            if t > 23:
                t = 0
            rst['date'] = "%s %s:%s" % (temp[0], str(t), temp2[1])
        # get company name
        rst['company'] = soup.select('#content > div.end_ct > div > div.press_logo > a > img')[0].get('alt')
        # get contents
        rst['cont'] = soup.select('#articeBody')[0].text
        return(rst)


    def form3(self, url, soup): # http://sports.news.naver.com # redirect
        rst = dict()
        rst['url'] = url
        # get title
        rst['title'] = soup.select('#content > div > div.content > div > div.news_headline > h4')[0].text
        # get date
        rst['date'] = soup.select('#content > div > div.content > div > div.news_headline > div > span')[0].text
        if '기사입력' in rst['date']:
            rst['date'] = re.sub('기사입력','',rst['date'])
        if '오전' in rst['date']:
            rst['date'] = re.sub('오전','',rst['date'])
        if '오후' in rst['date']:
            temp = rst['date'].split('오후')
            temp2 = temp[1].split(':')
            t = int(temp2[0]) + 12
            if t > 23:
                t = 0
            rst['date'] = "%s %s:%s" % (temp[0], str(t), temp2[1])
        # get company name
        rst['company'] = soup.select('#pressLogo > a > img')[0].get('alt')
        # get contents
        rst['cont'] = soup.select('#newsEndContents')[0].text.decode('utf-8', 'replace')
        print(rst)
        print('-'*50)
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
                news = self.form1(url, soup)

            # http://entertain.naver.com
            elif 'http://entertain.naver.com' in response.url:
                news = self.form2(url, soup)

            # http://sports.news.naver.com
            elif 'http://sports.news.naver.com' in response.url:
                news = self.form3(url, soup)

            if self.conn != 0:
                self.insertNews(news)
            return(news)
        else:
            print("getNewsInfo ERROR\t" + str(response.status_code) + '\t' + url)

    def getNewsContCrawling(self, url): #url을 db에서 받아와서 컨텐츠 수집
        for news in url:
            print("news:\t" + news)
            self.news.append(self.getNewsInfo(news))

    def newsCrawling(self, newsList = True, newsCont = True):
        # step1. 해당조건의 뉴스기사 검색 URL 생성
        url = self.getUrl()
        print(url)
        if newsList:
            # step2. 뉴스 기사 검색을 통해서 기사 URL list 생성
            while 1:
                # URL check
                if(url[0:6] != "https:"):
                    url = "https:" + url

                # get single new url & next page url. => return (next page)
                url = self.getResource(url)
                if(url == None):
                    break

        if newsCont:
            for news in self.newsUrl:
                print("news:\t" + news)
                self.news.append(self.getNewsInfo(news))

    def setDBToNewsUrl(self):
        self.newsUrl = self.selectNewsList()

    def setDBToNewsUrlUseQuery(self):
        self.newsUrl = self.selectNewsListUseqUery()

    ############################## search function ##############################
    def removeWhiteSpace(self, string):
        pattern = re.compile(r'\s+')
        return(re.sub(pattern, '', string))


    def searchKeyword(self, strings):
        newsTitle = list()
        newsCont = list()
        keywordList = list()

        rst = list()

        # 공백 제거 (제목, 내용)
        for oneNews in self.news:
            print(oneNews)
            try:
                newsTitle.append(self.removeWhiteSpace(oneNews['title']))
            except TypeError as e:
                newsTitle.append('empty')
            try:
                newsCont.append(self.removeWhiteSpace(oneNews['cont']))
            except TypeError as e:
                newsCont.append('empty')

        # 공백 제거 (string)
        for string in strings:
            keywordList.append(self.removeWhiteSpace(str(string)))

        # keywordList을 긴거 순으로 정렬
        keywordList.sort(key = len, reverse = True)


        for idx, cont in enumerate(newsCont):
            temp = dict()
            for string in keywordList:
                temp[string] = cont.count(string)
                if temp[string]:
                    print(string, str(temp[string]))
                newsCont[idx] = re.sub(string, '', cont)
            print('-'*30)
            rst.append(temp)
        return(rst)


    ############################## SQL function ##############################
    def sqlConnect(self, host, user, pw):
        print("DB connect...")
        self.conn = pymysql.connect(host=host,user=user,password=pw,charset='utf8mb4')


    def selectNewsList(self):
        try:
            with self.conn.cursor() as cursor:
                sql = 'SELECT distinct A.url FROM tobigs.news_list as A LEFT JOIN tobigs.news as B ON A.url = B.url WHERE B.url is null AND A.query = %s AND A.start = %s AND A.end = %s;'
                cursor.execute(sql, (self.myKeyword, self.start, self.end))
            rows = [row[0] for row in cursor.fetchall()]
            return(rows)
        except Exception as e:
            print("DB SELECT ERROR" + e)

    def selectNewsListUseqUery(self):
        try:
            with self.conn.cursor() as cursor:
                sql = 'SELECT distinct A.url FROM tobigs.news_list as A LEFT JOIN tobigs.news as B ON A.url = B.url WHERE B.url is null AND A.query = %s;'
                cursor.execute(sql, (self.myKeyword))
            rows = [row[0] for row in cursor.fetchall()]
            return(rows)
        except Exception as e:
            print("DB SELECT ERROR" + e)

    def selectKeywordPeriod(self, query):
        try:
            with self.conn.cursor() as cursor:
                sql = 'SELECT keyword, start, end FROM tobigs.keyword_period WHERE keyword = %s;'
                cursor.execute(sql, (query))
            columns = cursor.description
            rows = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            return(rows)
        except Exception as e:
            print("DB SELECT ERROR" + e)

    def selectNewsInfo(self):
        try:
            with self.conn.cursor() as cursor:
                sql = 'SELECT id, url, title, content, date, company FROM tobigs.news WHERE query = %s AND start = %s AND end = %s'
                cursor.execute(sql, (self.myKeyword, self.start, self.end))
            columns = cursor.description
            rows = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            return(rows)
        except Exception as e:
            print("DB SELECT ERROR" + e)


    def selectNewsUrl(self,newsid):
        try:
            with self.conn.cursor() as cursor:
                sql = 'SELECT url FROM tobigs.news WHERE id = %s'
                cursor.execute(sql, (newsid))
            columns = cursor.description
            rows = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
            return (rows[0])
        except Exception as e:
            print("DB SELECT ERROR" + e)

    def selectKeywordNewsIgnoreDate(self):
        try:
            with self.conn.cursor() as cursor:
                sql = 'SELECT title, date(date) as date from tobigs.news where query = %s'
                cursor.execute(sql, (self.myKeyword))
            columns = cursor.description
            rows = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            return(rows)
        except Exception as e:
            prunt("DB SELECT ERROR" + e)

    def insertNewsList(self, url):
        try:
            with self.conn.cursor() as cursor:
                sql = 'INSERT IGNORE INTO tobigs.news_list (query, start, end, url) VALUES (%s, %s, %s, %s)'
                cursor.execute(sql, (self.myKeyword, self.start, self.end, url))
            self.conn.commit()
        except Exception as e:
            print("DB INSERT ERROR" + e)


    def insertNews(self, news):
        try:
            with self.conn.cursor() as cursor:
                sql = 'INSERT IGNORE INTO tobigs.news (url, title, content, date, company, query, start, end) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(sql, (news['url'], news['title'], news['cont'].strip(), news['date'], news['company'], self.myKeyword, self.start, self.end))
            self.conn.commit()
        except Exception as e:
            print("DB INSERT ERROR" + e)

    def sqlClose(self):
        print("DB close...")
        if type(self.conn) == pymysql.connections.Connection:
            self.conn.close()
        else:
            print("DB is not connected.") #<class 'pymysql.connections.Connection'>


