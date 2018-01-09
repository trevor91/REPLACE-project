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


def getNewsUrl(newsId):
	obj = keyword(query, start, end)
	obj.sqlConnect(host, id, pw)
	rst = obj.selectNewsUrl(newsId)
	obj.sqlClose()
	return (rst)

if __name__ == '__main__':

	# host 	= sys.argv[1]
	# id 	= sys.argv[2]
	# pw 	= sys.argv[3]
	
	query = "북한"

	# query = "박근혜"
	# temp = [("2017.04.12","2017.04.15"),("2017.04.17","2017.04.19")]
	temp = [("2017.04.10","2017.04.20"),("2017.04.24","2017.04.26"),("2017.04.29","2017.04.29"),("2017.05.14","2017.05.14"),("2017.05.21","2017.05.21"),("2017.05.23","2017.05.23"),("2017.05.29","2017.05.29"),("2017.05.31","2017.05.31"),("2017.06.08","2017.06.08"),("2017.06.20","2017.06.20"),("2017.07.04","2017.07.07"),("2017.07.13","2017.07.13"),("2017.07.25","2017.07.25"),("2017.07.27","2017.07.29"),("2017.08.03","2017.08.03"),("2017.08.08","2017.08.14"),("2017.08.26","2017.08.26"),("2017.08.29","2017.08.30"),("2017.09.03","2017.09.05"),("2017.09.07","2017.09.10"),("2017.09.13","2017.09.13"),("2017.09.15","2017.09.16"),("2017.09.20","2017.09.20"),("2017.09.22","2017.09.26"),("2017.10.10","2017.10.10"),("2017.10.12","2017.10.13"),("2017.10.16","2017.10.16"),("2017.11.21","2017.11.22"),("2017.11.27","2017.11.29"),("2017.12.08","2017.12.08"),("2017.12.21","2017.12.21")]
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

