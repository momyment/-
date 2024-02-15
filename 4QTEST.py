import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

#네이버 웹 드라이버 시작
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "http://www.naver.com/"
driver.get(url)

#검색어 입력 상자 찾기
search_box = driver.find_element(By.NAME, "query")

#검색어 입력
search_box.send_keys("삼쩜삼")
search_box.send_keys(Keys.RETURN)

time.sleep(2)

#검색결과에서 바로 뉴스가 나오지 않아 옆에 버튼으로 뉴스탭 노출
next_button = driver.find_element(By.CLASS_NAME, 'btn_next')
next_button.click()

time.sleep(2)

# 뉴스탭 선택
news_tab = driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/div[1]/div/div[1]/div[8]/a')
news_tab.click()
time.sleep(2)

#최신순 선택
new = driver.find_element(By.XPATH, '//*//*[@id="snb"]/div[1]/div/div[1]/a[2]')
new.click()
time.sleep(2)


def crawling(count):
    titles_and_urls = []
    
    #count는 크롤링하고자 하는 페이지 수, 예를 들어 count가 2이면 처음에 로드된 페이지와 그 다음 페이지까지 총 2페이지의 뉴스를 크롤링
    for _ in range(count):
        #a.new_tit 에 해당하는 제목을 찾음
        items = driver.find_elements(By.CSS_SELECTOR, 'a.news_tit')
        #찾은 제목을 text로 가공
        titles = [item.text for item in items]
        #a.new_tit 에 해당하는 URL을 가지고 옴
        urls = [item.get_attribute('href') for item in items]
        # 가지고 온 제목,URL 을 하나로 묶음
        titles_and_urls.extend(list(zip(titles, urls)))
        
        time.sleep(2)
    #가지고 온 제목, URL을 호출
    return titles_and_urls
#제목, URL 을 2번 다음 페이지까지 크롤링
titles_and_urls = crawling(2)

# CSV 파일로 저장
with open('4Qresults.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['제목', 'URL'])
    writer.writerows(titles_and_urls)

print("저장되었습니다.")
