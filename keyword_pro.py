from Keyword import keyword

from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == '__main__':
	
	query	= ''
	start	= '2017.03.29'
	end 	= '2017.07.31'

	key1 = keyword(query, start, end)
	key1.sqlConnect('','','')
	key1.newsCrawling(newsList = True, newsCont = False)
	key1.sqlClose()
	print('-'*50)
	
	# temp = key1.getNews()
	# print(len(temp))
	# for idx, s in enumerate(temp):
	# 	print(s)
	# 	if idx == 5:
	# 		break
	# print('-'*50)
	

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
