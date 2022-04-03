from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import openpyxl

#1. 드라이버 옵션 설정 및 구동
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('/Users/dolpong/Desktop/크롤링/naver_news/chromedriver', options= options)

#url 접속
news_url = "https://news.naver.com/main/ranking/read.naver?m_view=1&includeAllCount=true&mode=LSD&mid=shm&sid1=001&oid=052&aid=0001721123&rankingType=RANKING"
driver.get(news_url)
time.sleep(5)


while True:
    #더보기 버튼 안 나올때까지 반복
    more = driver.find_element(By.CLASS_NAME, "u_cbox_page_more")
    if more.is_displayed():
        more.click()
        time.sleep(0.5)
    else:
        print("더보기 버튼 없음")
        break

# 페이지 소스 저장
html = driver.page_source
bs = BeautifulSoup(html, 'lxml')

#코멘트, 날짜, 공감, 비공감 수 파싱
comments = bs.find_all('span', class_='u_cbox_contents')
dates = bs.find_all('span', class_='u_cbox_date')
likes = bs.find_all('em', class_='u_cbox_cnt_recomm')
unlikes = bs.find_all('em', class_='u_cbox_cnt_unrecomm')

#데이터 프레임으로 저장
data = []
for comment, date, like, unlike in zip(comments, dates, likes, unlikes):
    data.append([comment.get_text(), like.get_text(), unlike.get_text(), date.get_text()])
df = pd.DataFrame(data, columns=['comment', 'like', 'unlike', 'date'])

#엑셀로 저장
df.to_excel('/Users/dolpong/Desktop/크롤링/naver_news/result.xlsx')


