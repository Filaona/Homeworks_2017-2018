from flask import Flask
from flask import url_for, render_template, request
from requests import get
import re
import html
import build_dorev
import operator



app = Flask(__name__)


def weather():
    page = get('https://yandex.ru/pogoda/skopje')
    page.encoding = 'utf-8'
    print(page.text)
    weather = re.search('<div class="temp fact__temp"><span class="temp__value">.*?</span>'
                        '<span class="temp__unit i-font i-font_face_yandex-sans-text-medium">°</span></div></a>'
                        '<div class="fact__condition day-anchor i-bem" data-bem=.*?>.*?</div>', page.text)
    weather = re.sub('<.*?>', '', weather.group())
    weather = re.sub('°', '°  ', weather)
    weather = weather.split('  ')
    return weather


@app.route('/')
def index():
    urls = {'Игра в ять ': url_for('testing'),
            'Главная страница Лента.ру в дореволюционной орфографии': url_for('site')}
    return render_template('index.html', weather=weather(), urls=urls)


def processing_page():
    page = get('https://lenta.ru/')
    body = re.compile('<body.*?Все материалы', flags=re.DOTALL)
    tags = re.compile('<.*?>', flags=re.DOTALL)
    space = re.compile('\s', re.DOTALL)
    java_func = re.compile('{.*?}', flags=re.DOTALL)
    #junk = re.compile('//<.*?>', flags=re.DOTALL)
    page = re.search(body, page.text)
    page = re.sub(tags, ' ', page.group())
    page = re.sub(java_func, ' ', page)
    page = re.sub(space, ' ', page)
    #page = re.sub(junk, ' ', page)
    #page = re.sub('[\n/]', '', page)
    return html.unescape(page).strip()


@app.route('/success')
def success():
    answers = ''
    for i in range(1, 11):
        if 'quest' + str(i) in request.values:
            if request.values['quest' + str(i)] == 'var1':
                answers += '1'
            else:
                answers += '2'
        else:
            answers += '0'
    right_answers = '2112212221'
    succ = 0
    for i in range(0, len(right_answers)):
        if right_answers[i] == answers[i]:
            succ += 1
    return render_template('success.html', success=succ, url_testing=url_for('testing'), url_index=url_for('index'))


@app.route('/site')
def site():
    dorev, stats = build_dorev.use_mystem(processing_page())
    stats_list = sorted(iter(stats.items()), key=operator.itemgetter(1))
    return render_template('site.html', dorev=dorev, url_index=url_for('index'), freq_words=stats_list[-10:])


@app.route('/testing')
def testing():
    return render_template('testing.html', url_index = url_for('index'))
    pass


@app.route('/result')
def result():
    dorev, stats = build_dorev.use_mystem(request.args['word'])
    return render_template('result.html', weather=weather(), dorev=dorev, word=request.args['word'],
                           url_index=url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)