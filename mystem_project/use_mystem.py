import os

def use_mystem(name_article, date, path_article):
    os.system(r'/home/filaona/PycharmProjects/mystem_project/mystem ' + ' -dic ' + '--format text '+ path_article + name_article + '.txt ' + 'Газета' + os.sep + 'mystem_plain' + os.sep + date[-4:] + os.sep + date[-7:-5] + os.sep + name_article +'.txt')
    os.system(r'/home/filaona/PycharmProjects/mystem_project/mystem ' + ' -dic ' + '--format xml '+ path_article + name_article + '.txt ' + 'Газета' + os.sep + 'mystem_xml' + os.sep + date[-4:] + os.sep + date[-7:-5] + os.sep + name_article + '.xml')
