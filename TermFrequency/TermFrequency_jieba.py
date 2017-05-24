#encoding=utf-8
import pyodbc
import jieba
from collections import defaultdict
from operator import itemgetter
import re

def readAccess(str):
    database = '../Data/ke2016_sample_data.accdb'
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + database + ';'
    )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    file_list = [row.content for row in crsr.execute("SELECT * FROM ke2016_sample_news WHERE section like '%s' OR section like '%s'" % (str[0], str[1]))]
    return file_list

def calTermFrequency(line, word_tf):
    for seg in jieba.cut(line, cut_all=False):
        word_tf[seg] += 1

def main():
    jieba.set_dictionary('dict.txt.big') # for Chinese(Traditional)
    str = ['%財經%', '%產經%']
    file_list = readAccess(str)
    print('All of file :', len(file_list))

    word_tf = defaultdict(int)
    line_list = [[line for line in re.split('，|。| |、|<BR>●|<BR>|：', file)] for file in file_list]
    for line in line_list:
        for tmp_line in line:
            calTermFrequency(tmp_line, word_tf)

    print('length :', len(word_tf))
    word_tf_sort = sorted(word_tf.items(), key=itemgetter(1), reverse=True)
    print(word_tf_sort)

if __name__ == '__main__':
    main()