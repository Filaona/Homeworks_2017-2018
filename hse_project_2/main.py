import json
import os
from flask import Flask
from flask import url_for, render_template, request, redirect
import urllib.parse
from requests import get
import re

app = Flask(__name__)


@app.route('/')
def questionary():
    urls = {'статистика ': url_for('stats'),
            'статистика в формате json ': url_for('stat_json'),
            'поиск': url_for('search')}
    return render_template('questionary.html', urls=urls)


@app.route('/thanks')
def thanks():
    for i in range(1, 7):
        if 'quest' + str(i) in request.values:
            pass
        else:
            return redirect(url_for('questionary'))
    if request.args:
        if request.args['name'] == '':
            name = 'путник'
        else:
            name = request.args['name']
    write_down()
    return render_template('thanks.html', name=name, url_questionary=url_for('questionary'))


def write_down():
    if os.path.isfile('results.json'):
        data = json.load(open('results.json'))
    else:
        data = []
    temp = []
    for i in range(0, 7):
        temp.append([])
    for i in range(1, 7):
        for j in range(1, 3):
            temp[i].append('')
    temp[0].append(request.args['name'])
    temp[0].append(request.args['age'])
    temp[0].append(request.args['city'])
    temp[0].append(request.args['language'])
    if 'education' in request.values:
        temp[0].append(request.values['education'])
    for i in range(1, 7):
        if request.values['quest' + str(i)] == 'var1':
            temp[i][0] = dic[i-1]['var1']
        else:
            temp[i][1] = dic[i-1]['var2']
    data.append(temp)
    json.dump(data, open('results.json', 'w'), ensure_ascii=False, indent=4)


def statistics(data):
    values = {}
    for i in range(1, 7):
        k = 0
        for j in range(0, len(data)):
            if data[j][i][0] != '':
                k += 1
        b = k/len(data)*100
        values[dic[i-1]['var1']] = int(b)
    return values

@app.route('/stats')
def stats():
    if os.path.isfile('results.json'):
        data = json.load(open('results.json'))
        values = statistics(data)
        return render_template('stats.html', isstat=True, url_questionary=url_for('questionary'),
                               values=values)
    else:
        return render_template('stats.html', isstat=False, url_questionary=url_for('questionary'))


@app.route('/json')
def stat_json():
    if os.path.isfile('results.json'):
        with open("results.json", "r", encoding='utf-8') as f:
            content = f.read()
        iscont = True
    else:
        iscont = False
        content = ''
    return render_template("json.html", iscont=iscont, content=content, url_questionary=url_for('questionary'))


@app.route('/search')
def search():
    return render_template('search.html', url_questionary=url_for('questionary'))


def get_page(query):
    s = get('http://accentonline.ru/%s/%s' % (urllib.parse.quote(query[0].upper()), urllib.parse.quote(query)))
    res = re.search('<span class="word-accent">.*?<', s.text)
    if res:
        res = res.group()[26:-1]
        res = re.sub('\&#x301;', "'", res)
    else:
        res = ''
    return res


@app.route('/results')
def results():
    if request.args['word']:
        res = get_page(request.args['word'].strip().lower())
        return render_template('results.html', res=res, url_search=url_for('search'), word=request.args['word'],
                               url_questionary=url_for('questionary'))
    return redirect('search')


if __name__ == '__main__':
    dic = [{'var1':'алфАвит', 'var2':'алфавИт'},{'var1':'бАловать', 'var2':'баловАть'},
           {'var1':'брАла', 'var2':'бралА'}, {'var1':'вклЮчим', 'var2':'включИм'},
           {'var1':'пломбИровать', 'var2':'пломбировАть'}, {'var1':'чЕрпать', 'var2':'черпАть'}]
    app.run(debug=True)
