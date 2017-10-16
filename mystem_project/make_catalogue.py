import html
import re
import csv
import os
import use_mystem


def print_text(text, date, header, url_page, author, path_article):
    if not os.path.exists(path_article):
        os.makedirs(path_article)
        os.makedirs(os.path.join('Газета', 'mystem_plain', date[-4:], date[-7:-5]))
        os.makedirs(os.path.join('Газета', 'mystem_xml', date[-4:], date[-7:-5]))
        name_article = 'статья1'
    else:
        for n in range(1,1000):
            if os.path.exists(path_article + os.sep + 'статья' + str(n) + '.txt'):
                continue
            else:
                name_article = 'статья' + str(n)
                break
    with open(os.path.join('.',path_article, name_article + '.txt'), 'w',encoding='utf-8') as f:
        f.write('@au ' + author + '\n@ti ' + header + '\n@da ' + date + '\n@topic ' +
                '\n@url ' + url_page + '\n' + text)
    return name_article


def write_csv(date, name_article, author, header, url_page):
    with open(os.path.join('.', 'Газета', 'metadata.csv'), 'a', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

        writer.writerow([os.path.join(date[-4:], date[-7:-5], name_article + '.txt'), author, '', '', header, date,
                         'публицистика', '', '', '', '', 'нейтральный',
                         'н-возраст', 'н-уровень', 'районная', url_page, 'Красный Север', '', date[-4:],
                         'газета', 'Россия', 'Ямало-ненецкий АО', 'ru'])

def process_page(page, url_page, name_articles):

    reg_tag = re.compile('<.*?>', re.DOTALL)
    reg_space = re.compile('\s{2,}', re.DOTALL)

    reg_header = re.compile('<h1 class="news-title simple font-open-semibold">.*?</h1>',
                            flags=re.DOTALL)  # find header
    header = reg_header.search(page)
    if header:
        header = header.group()
        header = reg_space.sub('', header)
        header = html.unescape(reg_tag.sub('', header))

        if header not in name_articles:
            name_articles.add(header)
            reg_text = re.compile('<div class="description font-open-s-light nm-b">.*? '  # find text
                                      '<div class="author-photgrapher">', flags=re.DOTALL)
            text = reg_text.search(page)
            text = text.group()
            text = reg_space.sub('', text)
            text = html.unescape(reg_tag.sub('', text))

            reg_author = re.compile('<a href=".*?" class="author-name font-open-s">.*?</a>')  # find author
            author = reg_author.search(page)
            if author:
                author = author.group()
                author = html.unescape(reg_tag.sub('', author))
            else:
                author = 'Noname'

            reg_date = re.compile('<p class="date font-open-s-light">.*?</p>')  # find date </h1> <p class="date font-open-s-light">03.10.2017 15:28:00</p>
            date = reg_date.search(page)
            date = date.group()
            date = html.unescape(reg_tag.sub('', date)[:10])

            path_article = 'Газета' + os.sep + 'plain' + os.sep + date[-4:] + os.sep + date[-7:-5] + os.sep
            name_article = print_text(text, date, header, url_page, author, path_article)
            use_mystem.use_mystem(name_article, date, path_article)
            write_csv(date, name_article, author, header, url_page)
    return name_articles


def make_csv():
    os.makedirs('Газета')
    with open(os.path.join('./Газета', 'metadata.csv'), 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere', 'genre_fi',
                         'type', 'topic', 'chronotop', 'style', 'audience_age', 'audience_level', 'audience_size',
                         'source',
                         'publication', 'publisher', 'publ_year', 'medium', 'country', 'region', 'language'])