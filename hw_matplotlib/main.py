import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def db_1():
    conn1 = sqlite3.connect('response.db')
    c1 = conn1.cursor()
    c1.execute('DROP TABLE IF EXISTS words')
    c1.execute('CREATE TABLE IF NOT EXISTS words(id integer, lemma text, wordform text, glosses text)')
    i = 1
    for row in c.execute('SELECT * FROM wordforms'):
        c1.execute('INSERT INTO words VALUES (?, ?, ?, ?)', (i, row[0], row[1], row[2]))
        i += 1
    conn1.commit()
    conn1.close()


def db_2():
    file = open('glosses.txt', 'r')
    dic_gloss = {}
    for line in file:
        dic_gloss[line.split()[0]] = line.split()[2]
    file.close()

    i = 1
    conn2 = sqlite3.connect('response.db')
    c2 = conn2.cursor()
    c2.execute('DROP TABLE IF EXISTS glosses')
    c2.execute('CREATE TABLE IF NOT EXISTS glosses(id integer, gloss text, definition text)')
    for gloss in dic_gloss:
        c2.execute('INSERT INTO glosses VALUES (?, ?, ?)', (i, gloss, dic_gloss[gloss]))
        i += 1
    conn2.commit()
    conn2.close()


def db_3():
    conn3 = sqlite3.connect('response.db')
    c3 = conn3.cursor()
    dic_gloss = {}
    for row in c3.execute('SELECT * FROM glosses'):
        dic_gloss[row[1]] = row[0]
    dic_word = {}
    for row in c3.execute('SELECT * FROM words'):
        for gloss in row[3].split('.'):
            if gloss in dic_gloss:
                if row[0] in dic_word:
                    dic_word[row[0]].append(dic_gloss[gloss])
                else:
                    dic_word[row[0]] = [dic_gloss[gloss]]
    c3.execute('DROP TABLE IF EXISTS words_glosses')
    c3.execute('CREATE TABLE IF NOT EXISTS words_glosses(id_word integer, id_gloss integer)')
    for word in sorted(dic_word):
        for gloss in dic_word[word]:
            c3.execute('INSERT INTO words_glosses VALUES (?, ?)', (word, gloss))
    conn3.commit()
    conn3.close()


def plots():
    conn4 = sqlite3.connect('response.db')
    c4 = conn4.cursor()
    part_speech = {'ADJ', 'ADV', 'CONJ', 'DEM', 'INDEF', 'N', 'NUM', 'P', 'PART', 'POSS', 'PRON', 'PRV', 'PTCP', 'REL',
                   'V'}
    part_sp, addition = 0, 0
    for gloss in c4.execute('SELECT gloss FROM words_glosses LEFT OUTER JOIN glosses ON id_gloss=id'):
        if gloss[0] in part_speech:
            part_sp += 1
        else:
            addition += 1
    x = [part_sp, addition]
    y = np.arange(len(x))
    labels = ('Части речи', 'Вспомогательные элементы')
    plt.bar(y, x, color='g', align='center')
    plt.xticks(y, labels)
    plt.title('Количество глосс в разметке')
    plt.ylabel('Количество встретившихся глосс данного класса')
    plt.xlabel('Классы глосс')
    sns.set()
    plt.show()


if __name__ == '__main__':
    conn = sqlite3.connect('hittite.db')
    c = conn.cursor()
    db_1()
    conn.close()
    db_2()
    db_3()
    plots()
