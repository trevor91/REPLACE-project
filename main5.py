#lexRank
from lexrankr import LexRank

if __name__ == '__main__':


	rst = ""
	f = open("Data\\titles.txt","r", encoding='utf-8')
	lines = f.readlines()
	cnt = 0
	for line in lines:
	    rst += line
	    cnt += 1
	    if cnt == 1000: break;
	f.close()

	rst = rst.replace("\n",". ")

	lexrank = LexRank()
	lexrank.summarize(rst)
	summaries = lexrank.probe(10)
	for summary in summaries:
	    print(summary)
