import json
import os
import html


def change_left_gender(grammar, left_gender):
    if grammar.find('муж') != -1:
        left_gender[0] = 2
        left_gender[1] = 1
    else:
        left_gender[0] = 1
        left_gender[1] = 1
    return left_gender


def change_right_gender(json_dic, j, right_gender):
    k = j
    miss = 0
    while k+1 < len(json_dic):
        if len(json_dic[k+1]) > 1:
            if json_dic[k+1]['analysis'] != []:
                if json_dic[k+1]['analysis'][0]['gr'][:2] == 'S,':
                    if json_dic[k+1]['analysis'][0]['gr'].find('муж') != -1:
                        right_gender[0] = 2
                        right_gender[1] = k - j - miss
                    else:
                        right_gender[0] = 1
                        right_gender[1] = k - j - miss
                    break
                else:
                    k += 1
            else:
                k += 1
        else:
            k += 1
            miss += 1
    return right_gender


def adj(grammar, dorev, left_gender, right_gender):
    female = grammar.find('жен')
    male = grammar.find('муж')
    neutral = grammar.find('сред')
    if (female != -1 or neutral != -1) and male == -1:
        dorev = dorev[0:-1] + 'я'
    elif female == -1 and neutral == -1 and male != -1:
        pass
    else:
        if left_gender[0] == right_gender[0]:
            if left_gender[0] == 1:
                dorev = dorev[0:-1] + 'я'
        elif left_gender[1] >= right_gender[1]:
            if right_gender[0] == 1:
                dorev = dorev[0:-1] + 'я'
        else:
            if left_gender[0] == 1:
                dorev = dorev[0:-1] + 'я'
        print('left_gender = ', left_gender[0], left_gender[1], sep = ' ')
        print('right_gender = ', right_gender[0], right_gender[1], sep=' ')
        print(dorev)

    return dorev, left_gender, right_gender


def build_dorev(part, part1, json_dic, j, left_gender, right_gender):
    set_vowel = {"А", "а", "Е", "е", "Ё", "ё", "И", "и", "О", "о", "У", "у", "Ы", "ы", "Э", "э", "Ю", "ю", "Я", "я"}
    set_without_er = {"ъ", "ь", "й", html.unescape('&#1141;'), html.unescape('&#1110'), html.unescape('&#1123')}
    dorev = ''
    grammar = json_dic[j]['analysis'][0]['gr']
    if part != '':
        for i in range(0, len(part)):
            if part[i] not in set_vowel:
                dorev += part[i]
            else:
                if part[i] == 'ё':
                    dorev += 'е'
                elif part[i] == 'Ё':
                    dorev += 'Е'
                elif part[i] == 'и':
                    if i != len(part) - 1:
                        if part[i+1] in set_vowel or part[i+1] == 'й':
                            dorev += html.unescape('&#1110')
                        else:
                            dorev += 'и'
                    else:
                        dorev += 'и'
                elif part[i] == 'И':
                    if i != len(part) - 1:
                        if part[i+1] in set_vowel or part[i+1] == 'й':
                            dorev += html.unescape('&#1030')
                        else:
                            dorev += 'И'
                    else:
                        dorev += 'И'
                else:
                    dorev += part[i]
        html.unescape(dorev)
        if dorev[-1] not in set_vowel | set_without_er and dorev[-1].islower():
            dorev += 'ъ'
        else:
            if dorev[-1] == 'е' and grammar[:2] == 'S,':
                if grammar.find('пр,ед') != -1 or grammar.find('дат,ед') != -1:
                    dorev = dorev[:-1] + html.unescape('&#1123;')
            elif grammar[0] == 'A' or grammar.find('прич') != -1:
                wordform = part1 + dorev
                if wordform[-2:] in {html.unescape('&#1110') + 'е', 'ы' + 'е'}:
                    dorev, left_gender, right_gender = adj(grammar, dorev, left_gender, right_gender)
                elif wordform[-4:] == html.unescape('&#1110') + 'еся':
                        dorev, left_gender, right_gender = adj(grammar, dorev[:-2], left_gender, right_gender)
                        dorev += 'ся'
                elif wordform[-3:] == 'ого' and wordform not in {'этого', 'много', 'этакого'}:
                    dorev = dorev[:-3] + 'аго'
                elif wordform[-3:] == 'его' and wordform not in {'вашего','всего','его','моего','нашего','своего', 'сего','твоего'}:
                    if len(wordform) > 3:
                        if wordform[-4] in {"ж", "ш", "щ","ч"}:
                            dorev = dorev[:-3] + 'аго'
                        else:
                            dorev = dorev[:-3] + 'яго'
                    else:
                        dorev = dorev[:-3] + 'яго'
                elif wordform[-3:] == 'ося':
                    if wordform[-6] in {"ж", "ш", "щ", "ч"}:
                        dorev = dorev[:-5] + 'агося'
                    else:
                        dorev = dorev[:-5] + 'ягося'
    if grammar[:2] != 'S,':
        left_gender[1] += 1
        right_gender[1] -= 1
    else:
        left_gender = change_left_gender(grammar, left_gender)
        right_gender = change_right_gender(json_dic, j, right_gender)
    return html.unescape(dorev), left_gender, right_gender


def find_dorev():
    set_vowel = {"А", "а", "Е", "е", "Ё", "ё", "И", "и", "О", "о", "У", "у", "Ы", "ы", "Э", "э", "Ю", "ю", "Я", "я"}
    set_without_er = {"ъ", "ь", "й", html.unescape('&#1141;'), html.unescape('&#1110;'), html.unescape('&#1123')}
    result = ''
    dorev_dic = json.load(open('dorev_dic.json', 'r'))
    json_dic = json.load(open('file_result.json', 'r'))
    number = len(json_dic)
    left_gender = [0, 50]
    right_gender = change_right_gender(json_dic, -1, [0, 50])
    stats = {}
    for j in range(0, len(json_dic)):
        if j % 4 == 0:
            for i in range(0, int(j/number*100)):
                print('-', sep='', end='')
            print("%.1f" % (j/number*100), '%', sep='')
        if len(json_dic[j]) > 1:
            if json_dic[j]['analysis'] != []:
                coincidence = 0
                lexeme = json_dic[j]['analysis'][0]['lex']
                stats[lexeme] = stats.get(lexeme, 0) + 1
                wordform = json_dic[j]['text']
                for i in range(0, min(len(lexeme), len(wordform))):
                    if lexeme[i] == wordform[i]:
                        coincidence += 1
                    else:
                        break
                if lexeme in dorev_dic:
                    dorev = dorev_dic[lexeme]
                    if coincidence == len(wordform) and json_dic[j]['analysis'][0]['gr'].find('ADV') != -1:
                        part1 = dorev
                    else:
                        part1 = dorev[0:coincidence]
                    part2, left_gender, right_gender = build_dorev(wordform[coincidence:], part1, json_dic, j,
                                                                   left_gender, right_gender)
                    if part2 == '' and part1[-1] not in set_vowel | set_without_er:
                        part1 = part1 + 'ъ'
                    dorev = part1 + part2
                else:
                    dorev, left_gender, right_gender = build_dorev(wordform, '', json_dic, j, left_gender, right_gender)
                result = result + ' ' + dorev
            else:
                result = result + ' ' + json_dic[j]['text']
                left_gender[1] += 1
                right_gender[1] -= 1
        else:
            result = result + json_dic[j]['text'] + ' '
    return html.unescape(result), stats


def use_mystem(text):
    file_start = open('file_start.txt', 'w', encoding='utf-8')
    file_start.write(text.strip())
    file_start.close()
    os.system('/home/filaona/PycharmProjects/hw_addition/mystem ' + '-digc' + ' --format json' + ' file_start.txt'
              + ' file_result.json')
    return find_dorev()