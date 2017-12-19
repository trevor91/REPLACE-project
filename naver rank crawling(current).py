#naver 실시간 검색어 
import json, requests
from pandas.io.json import json_normalize
import time

start = time.clock()

r = requests.get('http://rank.search.naver.com/rank.js')
# print(r.text)
title = json.loads(r.text)['ts'] + '.json'
title = title.replace('-','').replace(':','').replace('+','')

with open(title, 'w') as outfile:
    json.dump(r.text, outfile, ensure_ascii=False)

end = time.clock() - start
proTime = 17-end
time.sleep(proTime)

