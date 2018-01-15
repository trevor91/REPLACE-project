#lexRank
from Keyword import keyword
from lexrankr import LexRank
import re
import sys

def getKeywordNews(host, id, pw, query, start, end):
	obj = keyword(query, start, end)
	obj.sqlConnect(host, id, pw)
	rst = obj.selectNewsInfo() # 기간 상관없이 해당 키워드에 해당하는 모든 뉴스를 get
	obj.sqlClose()
	return(rst)


def lexrank(rst):
	print("=" * 20)
	print(len(rst))
	print(rst[0])
	print("=" * 20)
	lexInputText = ""
	hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
	for news in rst:
		lexInputText += str(news['id'])
		parse = hangul.sub('', news['title'])
		parse = re.sub(' +', ' ', parse).strip()
		parse = re.sub('\.', '', parse)
		lexInputText += parse
		parse = hangul.sub('', news['content'])
		parse = re.sub(' +', ' ', parse).strip()
		parse = re.sub('\.', '', parse)
		lexInputText += parse
		lexInputText += ". "

	print("=" * 10 + "LEXRANK" + "=" * 10)
	lexrank = LexRank()
	lexrank.summarize(lexInputText)
	summaries = lexrank.probe(10)
	searchId = re.compile('[0-9]{5,6}')
	idList = []
	for summary in summaries:
		idList.append(searchId.search(summary).group())
	return(idList)


def simpleLexrank(arg):
	lexrank = LexRank()
	lexrank.summarize(arg)
	summaries = lexrank.probe(3)
	return(summaries)


def getNewsUrl(newsId):
	obj = keyword(query, start, end)
	obj.sqlConnect(host, id, pw)
	rst = obj.selectNewsUrl(newsId)
	obj.sqlClose()
	return (rst)

if __name__ == '__main__':

	host= sys.argv[1]
	id 	= sys.argv[2]
	pw 	= sys.argv[3]
	query = "북한"
	temp = [("2017.04.24","2017.04.26"),("2017.08.08","2017.08.14"),("2017.07.04","2017.07.07"),("2017.09.07","2017.09.10"),("2017.11.21","2017.11.22")]
	for start, end in temp:
		rst = getKeywordNews(host,id,pw,query,start,end)
		idList = lexrank(rst)
		print(idList)
		path = "/home/trevor/tot/"
		filename = query + start[5:].replace(".","") + end[5:].replace(".","") + ".txt"
		print(filename)
		with open(path + filename, "w") as f:
			for newsId in idList:
				f.writelines(str(getNewsUrl(newsId)) + "\n")
# 	text = """

# (서울=연합뉴스) 성서호 기자 = 25일 오후 12시 51분 11초 경북 포항시 북구 북쪽 7㎞ 지역(북위 36.10도·동경 129.35)에서 규모 2.0의 지진이 발생했다. 지진의 발생 깊이는 8㎞다.

# 기상청은 이 지진을 이달 15일 발생한 포항 지진(본진 규모 5.4)의 여진으로 파악했다. 앞서 규모 2.0 이상의 여진은 24일 새벽 1시 17분께 경북 포항시 북구 북쪽 7㎞ 지역에서 발생했다.

# 이로써 규모 2.0 이상의 여진은 총 66회로 늘었다. 규모 4.0∼5.0 미만이 1회, 3.0∼4.0 미만이 5회, 2.0∼3.0 미만이 60회였다.

	
# 	"""

# 	rst = simpleLexrank(text)
# 	print(rst)