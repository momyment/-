import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

#드라이브 검색 후 해당 URL로 뉴스 > 최신순 URL 로 진입 
#풀어서 할 수 있으면 풀어서 하자 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://www.naver.com"

driver.get(url)

search_box = driver.find_element_by_name("삼쩜삼")



def crawling(count):
    titles_and_urls = []
    
    #count는 크롤링하고자 하는 페이지 수, 예를 들어 count가 2이면 처음에 로드된 페이지와 그 다음 페이지까지 총 2페이지의 뉴스를 크롤링
    for _ in range(count):
        items = driver.find_elements(By.CSS_SELECTOR, 'a.news_tit')
        titles = [item.text for item in items]
        urls = [item.get_attribute('href') for item in items]
        titles_and_urls.extend(list(zip(titles, urls)))
        
        #next_button = driver.find_element(By.CLASS_NAME, 'btn_next')
        #next_button.click()
        time.sleep(2)
    
    return titles_and_urls

titles_and_urls = crawling(2)

# CSV 파일로 저장
with open('results.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['제목', 'URL'])
    writer.writerows(titles_and_urls)

print("저장되었습니다.")