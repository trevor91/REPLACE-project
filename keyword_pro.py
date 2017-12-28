from Keyword import keyword

from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == '__main__':
	
	### 한 시점에 대해서 20개 키워드를 각각 start, end를 통해서 기사를 수집하고.
	### 그 기사들을 기준으로. A라는 키워드 기사에 나머지 19개의 키워드 모두에대한 cosine similarity를 구함.

	# key1 = keyword(query, start, end)
	key1 = keyword()
	key1.sqlConnect('','root','')
	period = key1.selectKeywordPeriod("미세먼지")
	for s in period:
		print(s)
		key1.setKeyword(s["keyword"])
		key1.setStart(s["start"])
		key1.setEnd(s["end"])

		key1.newsCrawling(newsList = True, newsCont = False)
		# key1.setDBToNewsUrl()
		# key1.newsCrawling(newsList = False, newsCont = True)
	
	# key1.newsCrawling(newsList = True, newsCont = False)

	# key1.selectNewsList()
	
	# key1.setDBToNewsUrl()
	# key1.newsCrawling(newsList = False, newsCont = True)

	key1.sqlClose()
	print('-'*50)