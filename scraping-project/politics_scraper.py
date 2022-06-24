## Importing data
import numpy as np
import scrapy
import re
import requests
from bs4 import BeautifulSoup

## Information needed
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
url = 'https://reddit.com/r/politics/'
source = requests.get(url, headers = headers)
soup = BeautifulSoup(source.text, 'html.parser')

## Filtering through data
div = soup.find_all('div', class_ = 'y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE')
titles = []
for d in div:
    titles.append(d.a.text)

## Dictionary of number of times word is repeated in titles
dic = {}
for title in titles:
    words_numbers = re.sub("[!:/(),.]", " ", title)
    words_numbers_list = words_numbers.split(' ')
    for word_number in words_numbers_list:
        word = word_number.lower()
        if (word in dic.keys()) and (word):
            dic[word] += 1
        elif (word not in dic.keys()) and (word):
            dic[word] = 1

## Finding most used word
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
