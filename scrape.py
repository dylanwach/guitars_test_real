from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import send_mail
import send_mail
import urllib.request
import urllib.parse


username = "jaflood@davidson.edu"
password = "WlaH@5cNY5TmKQZnu"


def login(d):
    driver.find_element_by_name("user_session[login]").send_keys(username)
    driver.find_element_by_id("user_session_password").send_keys(password)
    driver.find_element_by_name("commit").click()

def get_links(driver1):
    # login(driver1)
    driver1.get("https://reverb.com/marketplace?product_type=electric-guitars&condition=used")
    # driver.get('https://reverb.com/marketplace?product_type=electric-guitars&page=5')
    time.sleep(1)
    html_source = driver1.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    all_links = re.findall(r'<a class="grid-card__inner" href="(.*?)"', str(soup))
    # print(all_links)
    return all_links


def get_prices_model(driver1, link, base):
    driver1.get(link)
    time.sleep(1)
    html_source = driver1.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    prices = re.findall(r'span class="price-display">(.*?)</span', str(soup))
    # print('Prices of same "model: " ' + str(prices))
    int_prices = []
    low = base / 2
    high = base * 2
    if len(prices) != 0:
        for i in prices:
            x = i.replace('$', '')
            x = x.replace(',', '')
            p = int(float(x))
            if low < p < high:
                int_prices.append(p)
    if len(int_prices) > 0:
        avg = sum(int_prices) / len(int_prices)
        # print('Average "model": ' + str(a))
        return avg


def get_prices_name(driver1, link, base):
    driver1.get(link)
    time.sleep(1)
    html_source = driver1.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    prices = re.findall(r'span class="price-display">(.*?)</span', str(soup))
    int_prices = []
    low = base / 2
    high = base * 2
    if len(prices) != 0:
        for j in prices:
            x = j.replace('$', '')
            x = x.replace(',', '')
            p = int(float(x))
            if low < p < high:
                int_prices.append(p)
    if len(int_prices) > 0:
        a = sum(int_prices) / len(int_prices)
        # print('Average "model": ' + str(a))
        return a


def into_searchable(title1):
    title = title1.split(' ')
    link = 'https://reverb.com/marketplace?query='
    title = '%20'.join(title)
    link = link + title + '&show_only_sold=true'
    # print(link)
    return link


def clean(title1):
    title = title1.lower()
    title = title.replace('used', '')
    title = title.replace('electric guitar', '')
    return title


def cart(s, l):
    in_cart = re.findall(r'this in their cart(.*?)/', str(s))
    if len(in_cart) != 0:
        print('IN CART')
        send_mail.send_email('Item in Cart', l)


def get_guitar(driver1, link):
    driver1.get(link)
    time.sleep(1)
    html_source = driver1.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    title1 = re.findall(r'&quot;title&quot;:&quot;(.*?)&quot', str(soup))
    title2 = re.findall(r'</a></li></ul><h1>(.*?)<', str(soup))
    title3 = re.findall(r'</a></div><h1>(.*?)<', str(soup))
    title = ''
    if len(title1) != 0:
        title = title1[0]
    elif len(title2) != 0:
        title = title2[0]
    elif len(title3) != 0:
        title = title3[0]
    else:
        print('fail')
        return
    cart(soup, link)
    model = re.findall(r'Model</td><td data-spec-groups="true"><ul class="collapsing-list collapsing-list--collapsed">'
                       r'<li class="collapsing-list__item"><a href="(.*?)</a', str(soup))[0].split('">')
    price = re.findall(r'<span class="price-display">(.*?)<', str(soup))[0]
    print("Price: " + price)
    price = price.replace(',', '')
    price = float(price.split('$')[1])
    if 3000 < price or 300 > price:
        return
    model1 = model[0].replace('amp;', '') + '&show_only_sold=true'
    # print(model1)
    model_price = get_prices_model(driver1, model1, price)
    # print(title)
    title = clean(title)
    print(title)
    link_search = into_searchable(title)
    name_price = get_prices_name(driver1, link_search, price)
    deal = False
    try:
        if name_price > (price + price*1.3):
            print('*****')
            print(str(price) + ' vs ' + str(name_price) + '\n')
            deal = True
    except:
        print('none')
    try:
        if model_price > (price + 30):
            print('*****')
            print(str(price) + ' vs ' + str(model_price) + '\n')
            deal = True
    except:
        print('none')

    if deal:
        return link

    '''
    try:
        brand = re.findall(r'Brand</td><td data-spec-groups="true"><ul class="collapsing-list collapsing-list--collapsed">'
                       r'<li class="collapsing-list__item"><a class="" href="(.*?)</a', str(soup))[0].split('">')[1]
        print(brand)
        brands = ['SGN']
        if brand in brands:
            print('Not a guitar')
    except:
        print('no linked brand')
    try:
        finish = re.findall(r'Finish</td><td data-spec-groups="true"><ul class="collapsing-list collapsing-list--collapsed">'
                       r'<li class="collapsing-list__item"><a class="" href="(.*?)</a', str(soup))[0].split('">')[1]
        print(finish)
    except:
        print('no finish')
    '''


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=r'chromedriver 3')
    # helper 1- gather links
    links = get_links(driver)
    # gets all guitars
    # to specify a subset if you want to look closer, put [x:y] after links. this will examine the xth through yth link
    deals = ''
    for i in links[10:20]:
        # print('----------')
        try:
            x = get_guitar(driver, i)
            if x is not None:
                deals += x + '\n\n'
                print('\n')
        # if there is deal the get guitar function will return the link of that guitar. after running through all it
        # should have all potential deals
        except:
            print('guitar failed')
            # if for some reason there is an error this wont stop the program
    print(deals)
    if len(deals) != 0:
        send_mail.send_email('Potential Deals:', str(deals))
