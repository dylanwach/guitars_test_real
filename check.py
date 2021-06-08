from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import send_mail


def do_check(driver, link, word):
    driver.get(link)
    time.sleep(1)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    items = re.findall(r'class="grid-card__title">(.*?)<', str(soup))
    links = re.findall(r'<a class="grid-card__inner" href="(.*?)"', str(soup))
    found = False
    count = 0
    found_links = ''
    f = open('already_found', 'r')
    x = f.read().split(', ')
    for name in items:
        if word in name.lower() and links[count] not in x:
            print(links[count])
            found = True
            found_links += word + ' found: ' + links[count] + '\n\n'
            x.append(links[count])
        count += 1
    f.close()
    x = ', '.join(x)
    f = open('already_found', 'w')
    f.write(x)
    f.close()
    return found, found_links


def check_words():
    driver1 = webdriver.Chrome(executable_path=r'../guitars/chromedriver 3')
    # put in desired url. right now set to pedals
    url = 'https://reverb.com/marketplace?product_type=effects-and-pedals&condition=used'
    # used boss for testing purposes. words_to_check is where you input desired words
    words_to_check = ['sweet tea', 'boss', '']
    results = ''
    found = ''
    for word in words_to_check:
        found, link = do_check(driver1, url, word)
        if found:
            results = results + str(link) + '\n '
        found += word + ' '
    print(results)
    if results != '':
        send_mail.send_email(found, str(results))


if __name__ == '__main__':
    check_words()