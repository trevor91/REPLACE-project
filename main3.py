# get data and convert the TOT data structure
import datetime, time
from Keyword import keyword
from collections import Counter
import re
import sys

def getKeywordNewsIgnoreDate(host, id, pw, query):
	obj = keyword(keyword = query)
	obj.sqlConnect(host, id, pw)
	rst = obj.selectKeywordNewsIgnoreDate() # 기간 상관없이 해당 키워드에 해당하는 모든 뉴스를 get
	obj.sqlClose()
	return(rst)


if __name__ == '__main__':

	host 	= sys.argv[1]
	id 		= sys.argv[2]
	pw 		= sys.argv[3]
	keywords= [""] 


	data = []
	#sql문을 where에 or를 통해서 한번에 실행하는게 속도상 매우 유리
	#현재는 하나의 키워드에대해서 한번에 쿼리를 날리고 이것을 합침 -> 수정 필요?
	for query in keywords:
		data.extend(getKeywordNewsIgnoreDate(host, id, pw, query))
	# print(data)
	timestamps = []
	for row in data:
		timestamps.append(int(time.mktime(row['date'].timetuple())))

	cnt = dict(Counter(timestamps))

	f = open("Data\\times.txt","w")
	for i in sorted(cnt):
		f.writelines("%s %s\n" % (cnt[i], i))
	f.close()

	sortData = sorted(data, key = lambda k: k['date'])
	f = open("Data\\titles.txt","w", encoding = "UTF-8")
	hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') 
	for i in sortData:
		parse = hangul.sub('', i['title'])
		# parse = re.sub("[-=.#/?:$}]"," ",i['title'])
		parse = re.sub(' +',' ',parse).strip()
		f.writelines("%s\n" % (parse))
	f.close()