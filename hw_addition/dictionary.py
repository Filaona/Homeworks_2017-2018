from bs4 import BeautifulSoup
from requests import get
import re
import json



def get_words(page_let, dic):
    soup = BeautifulSoup(page_let.text, 'lxml')
    path = soup.dl.table.tr.td.contents[3].find_all('tr')
    for row in range(1, len(path)):
        dorev = str(path[row].contents[3])
        tags = re.compile('<.*?>', flags=re.DOTALL)
        dorev = re.sub(tags, '', str(dorev))
        dorev = dorev.split()[0].strip(', ')
        dorev = re.sub("'", '', dorev)
        dic[path[row].contents[1].string] = dorev
    print('imalive')
    return dic


def get_pages():
    dic = {}
    page = get('http://www.dorev.ru/ru-index.html?l= c0')
    dic = get_words(page, dic)
    soup = BeautifulSoup(page.text, 'lxml')
    path = soup.dl.table.tr.td.contents[2].tr.find_all('td')
    for number in range(1, len(path)):
        #print(path[number].a['href'])
        page_let = get('http://www.dorev.ru/' + path[number].a['href'])
        dic = get_words(page_let, dic)
    f = open('dorev_dic.json', 'w')
    json.dump(dic, f, ensure_ascii = False)





if __name__ == '__main__':
    get_pages()