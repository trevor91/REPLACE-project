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

	# host 	= sys.argv[1]
	# id 		= sys.argv[2]
	# pw 		= sys.argv[3]
	host = "13.124.46.181"
	id = "root"
	pw = "tobigs"
# 	keywords= ["포항지진","지진","경주 지진","수능 연기","포항","포항지진피해","여진","포항여진","대구지진","일본지진","구례 지진","북한 지진","중국 지전","멕시코 지진","지진 규모","광교 화재","대구 지진"]
# 	keywords = ["북한","랜섬웨어","불상발사체","북한 미사일 발사","북한 미사일","지대함 미사일", "오토 웜비어","북한 중대발표","김정은","미사일","북한 핵실험","귀순 북한 병사","jsa","귀순","북한군 귀순"]
# 	keywords =	["최순실","세월호","김관진","박근혜","영장심사","박근혜 구속","안철수","우병우","기소","심상정","유승민","홍준표","고영태","구속기소","대선후보","문재인","대선","김기춘","정유라","한민구","이재용","이건희",	"삼성전자","집행유예"]
	keywords = ["최순실", "세월호","박근혜","박근혜 구속", "우병우", "기소","구속기소",
				"김기춘", "이재용",]
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

	f = open("Data\\times","w")
	for i in sorted(cnt):
		f.writelines("%s %s\n" % (cnt[i], i))
	f.close()

	sortData = sorted(data, key = lambda k: k['date'])
	f = open("Data\\titles","w", encoding = "UTF-8")
	hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') 
	for i in sortData:
		parse = hangul.sub('', i['title'])
		parse = re.sub(' +',' ',parse).strip()
		f.writelines("%s\n" % (parse))
	f.close()