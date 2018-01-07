# Tobigs-project

네이버 실검을 기준으로 이슈가 되었던 키워드를 검색 및 이슈였던 기간의 뉴스를 크롤링하고 Topics over time알고리즘을 통해서 기간마다 topic을 추출한다.
기간별 topic을 통해서 어떠한 사건의 흐름을 알 수 있는 대표기사를 추출하는것이 이 프로젝트의 목표.

### step1.
> main.py을 통해서 해당 키워드가 실검에 올라온것을 확인 및 DB에 저장
>> keyListFileName 변수에 저장된 키워드 리스트들의 실검 등장 시간을 csv로 저장
>> 저장된 csv를 통해서 main.py는 seqDate.R를 호출하여 2017.01.02, 2017.01.03, 2017.01.04같이 연속된 데이터를 start는 2017.01.02, end는 2017.01.04의 형태로 변경 (연속된게 없으면 start와 end는 같은값을 가짐)
>> 수정한 파일을 DV에 저장하고 csv파일은 삭제


### step2.
> main2.py를 통해서 기사를 크롤링
>> step1을 통해서 저장된 키워드(query), 기간(start, end)를 통해서 해당 키워드를 통해서 해당 기간에 나온 뉴스를 수집함
>> getNewsUrlList()를 통해서 해당 키워드를 해당 기간만큼 검색하여 등장했던 기사의 URL들을 전부 수집하고,
>> newsCrawling()을 통해서 위에서 수집한 기사의URL들을 참조하여 기사의 내용을 수집

### step3.
> main3.py는 TOT알고리즘을 실행할 수 있는 Data형태로 변경
>> step2를 통해서 수집된 기사의 시간, 제목을 가져와서 tot를 돌리기 적합한 형태로 저장
>>> TOT를 사용하기위한 code는 <a href = 'https://github.com/ahmaurya/topics_over_time'>이곳</a>을 참조하였음