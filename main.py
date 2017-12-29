from Keyword import keyword
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys


## get news url list

# 해당 키워드에 해당하는것, 기간 전체를 클롤링.
def getNewsURLListUseDB(host, iden, pw, query):
	key1 = keyword()
	key1.sqlConnect(host, iden, pw)
	period = key1.selectKeywordPeriod(query)
	for s in period:
		print(s)
		key1.setKeyword(s["keyword"])
		key1.setStart(s["start"])
		key1.setEnd(s["end"])

		key1.newsCrawling(newsList = True, newsCont = False)
	key1.sqlClose()

# 해당 키워드에 해당 기간만 크롤링.
def getNewsUrlList(host, iden, pw, query, start, end):
	key1 = keyword(query, start, end)
	key1.sqlConnect(host, iden, pw)
	
	key1.newsCrawling(newsList = True, newsCont = False)

	key1.sqlClose()


## news crawling

# 현재 설정된 query, start, end를 조건으로 기사 크롤링
def newsCrawling(host, iden, pw, query, start, end):
	key1 = keyword(query, start, end)
	key1.sqlConnect(host, iden, pw)
	key1.setDBToNewsUrl() #set news url
	key1.newsCrawling(newsList = False, newsCont = True)
	key1.sqlClose()

# 현재 설정된 query를 조건으로 기사 크롤링
def newsCrawlingUseQuery(host, iden, pw, query, start, end):
	key1 = keyword(query, start, end)
	key1.sqlConnect(host, iden, pw)
	key1.setDBToNewsUrlUseQuery() #set news url
	key1.newsCrawling(newsList = False, newsCont = True)
	key1.sqlClose()


if __name__ == '__main__':
	host 	= sys.argv[1]
	iden 	= sys.argv[2]
	pw 		= sys.argv[3]

	query	= sys.argv[4]
	start	= sys.argv[5]
	end 	= sys.argv[6]
	
	# getNewsURLListUseDB(host, iden, pw, query)
	getNewsUrlList(host, iden, pw, query, start, end)
	# newsCrawling(host, iden, pw, query, start, end)
	# newsCrawlingUseQuery(host, iden, pw, query, start, end)
	
def temp():
	pass
	# testDic = key1.searchKeyword(testKeyword)
	# # print(testDic)
	# vect = DictVectorizer(sparse=False)
	# tfidf_matrix = vect.fit_transform(testDic)
	
	# print('-'*50)
	# print(tfidf_matrix)
	# print('-'*50)
	# print(tfidf_matrix[0:1])
	# print('='*50)

	# for i in range(len(tfidf_matrix)):
	# 	print('*'*50)
	# 	rst = cosine_similarity(tfidf_matrix[i:(i+1)], tfidf_matrix)
	# 	print(rst)
	# # next refer.
	# # https://datascienceschool.net/view-notebook/3e7aadbf88ed4f0d87a76f9ddc925d69/
