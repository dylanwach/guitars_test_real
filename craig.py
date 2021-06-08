from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import send_mail


def do_check(driver, link):
    driver.get(link)
    time.sleep(1)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    #print(str(soup))
    # only checking if one of the top 4 is new, otherwise slow checking a lot of old stuff.
    # basically, we know that if we havent checked in a while (i.e. before a run of the system) then there will be a lot of new ones
    # but if we are running automatically, realistically only 1 will pop up (at the very extreme 4) within our 30 second period
    # so only checking the most recent 4 would be worth it, saving lots of computing time
    string = re.findall(r'class="result-title hdrlnk" data-id="(.*?)</a>', str(soup))[:4]
    prices = re.findall(r'"result-price">(.*?)<', str(soup))[:8]
    ids = [x.split('"')[0] for x in string]
    links = [x.split('"')[2] for x in string]
    names = [x.split('>')[1] for x in string]

    found_links = ''
    f = open('already_craig', 'r')
    x = f.read()
    count = 0
    found = False
    for idd in ids:
        if idd not in x:
            found = True
            found_links += names[count] + ': ' + prices[2*count] + ' ' + links[count] + '\n\n'
        count += 1
    f.close()
    f = open('already_craig', 'w')
    f.write(str(ids))
    f.close()
    new = False
    return found, found_links


def check_craig():
    driver1 = webdriver.Chrome(executable_path=r'../guitars/chromedriver 3')
    # put in desired url. right now set to pedals
    url = 'https://washingtondc.craigslist.org/search/msg?query=-cymbal+-horns+-violin+-drum+-flute+-piano+-horn+-keybord+-ukelele+-saxophone+-trumpet+-alto+-sax&purveyor-input=owner'
    url_base = 'https://washingtondc.craigslist.org/search/msg?query='
    extra = '-cymbal+-horns+-violin+-drum+-flute+-piano+-horn+-keybord+-ukelele+-saxophone+-trumpet+-alto+-sax&purveyor-input=owner'
    # used boss for testing purposes. words_to_check is where you input desired words
    results = 'New items: \n'
    found, link = do_check(driver1, url_base)
    if found:
        results = results + str(link) + '\n '
    else:
        return
    if results != '':
        send_mail.send_email('Found new items ', str(results))


if __name__ == '__main__':
    check_craig()

# <a class="result-title hdrlnk" data-id="7322064987" href="https://washingtondc.craigslist.org/doc/msg/d/washington-gibson-les-paul-classic/7322064987.html" id="postid_7322064987">Gibson Les Paul Classic electric guitar 2020-21 model</a>
# <a class="result-title hdrlnk"