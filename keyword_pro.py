from Keyword import keyword

if __name__ == '__main__':
	query	= '비트코인'
	start	= '2017.04.04'
	end 	= '2017.04.05'
	
	key1 = keyword(query, start, end)

	key1.newsCrawling()
	print('-'*50)
	
	print(key1.getNews())

	# key1.searchKeyword('거래소', '코인', '비트코인', '이더리움', '리플')