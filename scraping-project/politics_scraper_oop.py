## Importing data
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import numpy as np
import re
from bs4 import BeautifulSoup

class RedditScraper:
    def __init__(self, url):
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        self.url = url

    def scraping(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("window-size = 1920,1080")
        s = Service('/Users/charlie/Desktop/chromedriver')
        driver = webdriver.Chrome(service = s, options = options)
        page_length = driver.execute_script("return window.screen.height;")
        length = 0
        i = 1
        driver.get(self.url)
        while length <= 50:
            soup = BeautifulSoup(driver.page_source, 'lxml')
            titles = soup.find_all('h3', class_ = '_eYtD2XCVieq6emjKBH3m')
            length = len(titles)
            driver.execute_script(f"window.scrollTo(0,{page_length}*{i});")
            i += 1
            time.sleep(1)

        ## Dictionary of words and number of times they were repeated
        dic = {}
        for title in titles:
            words_numbers = re.sub("[!:/(),.]", " ", title.text)
            words_numbers_list = words_numbers.split(' ')
            for word_number in words_numbers_list:
                word = word_number.lower()
                if (word in dic.keys()) and (word):
                    dic[word] += 1
                elif (word not in dic.keys()) and (word):
                    dic[word] = 1

        ## Finding most repeated words, returning them and the ammount of times they were repeated
        most = []
        keys = list(dic.keys())
        values = list(dic.values())
        values_unique = np.unique(np.array(values))
        values_unique_sorted = values_unique[::-1]
        for i in values_unique_sorted:
            keys = [k for k, v in dic.items() if v == i]
            for key in keys:
                most.append(f'{key} {i}')
        print(most)


politics = RedditScraper('https://reddit.com/r/politics/')
print(politics.scraping())
