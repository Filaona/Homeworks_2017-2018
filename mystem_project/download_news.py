import urllib.request
import re
import time
from make_catalogue import process_page, make_csv



def get_page(name_pages, queue_pages, name_articles):
    time.sleep(2)
    url = 'https://ks-yanao.ru/'
    url_page = queue_pages.pop(0)
    try:
        response = urllib.request.urlopen(url_page)
        page = response.read().decode('utf-8')
        reg_href = re.compile('href=".*?"')
        for href in reg_href.findall(page):
            if (href.find('.html') != -1) or (href.find('arkhiv-po-datam') != -1):  # if link is relevant
                if href[6:-1] not in name_pages:  # if link is new
                    name_pages.add(url + href[6:-1])
                    queue_pages.append(url + href[6:-1])
        if url_page.find('html') != -1:  # if there is text on page
            name_articles = process_page(page, url_page, name_articles)
    except:
        pass
    return (name_pages, queue_pages, name_articles)


def run_queue(name_pages, queue_pages, name_articles):
    make_csv()
    while queue_pages != []:
            (name_pages, queue_pages, name_articles) = get_page(name_pages, queue_pages, name_articles)
    else:
        print('queue_pages is empty')



def queue_init():
    url = 'https://ks-yanao.ru/'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        main_page = response.read().decode('utf-8')
    reg_section = re.compile(r'\w*?/" class="menu-links font-cuprum root-item')  # reg for section of newspaper
    last_part = '" class="menu-links font-cuprum root-item'
    name_pages = set()
    name_articles = set()
    queue_pages = []
    for section in reg_section.findall(main_page):  # init queue and set
        section = section.replace(last_part, '')
        name_pages.add(url + section)
        queue_pages.append(url + section)
    return (name_pages, queue_pages, name_articles)



def main():
    (name_pages, queue_pages, name_articles) = queue_init()
    run_queue(name_pages, queue_pages, name_articles)


if __name__ == '__main__':
    main()


