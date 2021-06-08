from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import urllib.request
import urllib.parse


def get_links():
    req = urllib.request.Request("https://reverb.com/marketplace?product_type=electric-guitars&condition=used")
    soup = BeautifulSoup(str(req), 'lxml')
    print(type(soup))
    print(soup)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    print(respData)
    all_links = re.findall(r'com/p/(.*?)&', str(respData))
    print(all_links)
    return all_links


def get_prices_model(link):
    req = urllib.request.Request(link)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    prices = re.findall(r'span class="price-display">(.*?)</span', str(respData))
    print('Prices of same "model: " ' + str(prices))
    int_prices = []
    if len(prices) != 0:
        for i in prices:
            x = i.replace('$', '')
            x = x.replace(',', '')
            int_prices.append(float(x))
        a = sum(int_prices) / len(int_prices)
        print('Average "model": ' + str(a))


def get_prices_name(link):
    req = urllib.request.Request(link)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    prices = re.findall(r'span class="price-display">(.*?)</span', str(respData))
    int_prices = []
    if len(prices) != 0:
        for i in prices:
            x = i.replace('$', '')
            x = x.replace(',', '')
            int_prices.append(float(x))
        a = sum(int_prices) / len(int_prices)
        print('Average name: ' + str(a))


def into_searchable(title1):
    title = title1.split(' ')
    link = 'https://reverb.com/marketplace?query='
    title = '%20'.join(title)
    link = link+title+'&show_only_sold=true'
    print(link)
    return link


def get_guitar(link):
    req = urllib.request.Request(link)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    title1 = re.findall(r'&quot;title&quot;:&quot;(.*?)&quot', str(respData))
    title2 = re.findall(r'</a></li></ul><h1>(.*?)<', str(respData))
    title = ''
    if len(title1) == 1:
        title = title1[0]
    else:
        title = title2[0]
    #print(soup)
    model = re.findall(r'Model</td><td data-spec-groups="true"><ul class="collapsing-list collapsing-list--collapsed">'
                       r'<li class="collapsing-list__item"><a href="(.*?)</a', str(respData))[0].split('">')
    get_prices_model(model[0])
    print(title)
    link_search = into_searchable(title)
    get_prices_name(link_search)
    try:
        brand = re.findall(r'Brand</td><td data-spec-groups="true"><ul class="collapsing-list collapsing-list--collapsed">'
                       r'<li class="collapsing-list__item"><a class="" href="(.*?)</a', str(respData))[0].split('">')[1]
        print(brand)
        brands = ['SGN']
        if brand in brands:
            print('Not a guitar')
    except:
        print('no linked brand')
    try:
        finish = re.findall(r'Finish</td><td data-spec-groups="true"><ul class="collapsing-list collapsing-list--collapsed">'
                       r'<li class="collapsing-list__item"><a class="" href="(.*?)</a', str(respData))[0].split('">')[1]
        print(finish)
    except:
        print('no finish')


if __name__ == '__main__':
    links = get_links()
    quit()
    for i in links[4:5]:
        get_guitar(i)
        print('\n')
