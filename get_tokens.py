from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import pandas as pd


def get_links(driver, page):
    driver.get("https://reverb.com/marketplace?product_type=bass-guitars&condition=used&page=" + str(page))
    time.sleep(2)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    titles = re.findall(r'<h4 class="grid-card__title">(.*?)<', str(soup))
    return titles


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=r'../guitars/chromedriver')
    d = {}
    for i in range(1,100):
        titles = get_links(driver, i)
        for title in titles:
            words = title.split(' ')
            for word in words:
                if word not in d:
                    d[word] = 0
                d[word] += 1
    df = pd.DataFrame(d.items())
    df = df.sort_values(1, ascending=False)
    df.to_csv('bass_guitars_words.csv')