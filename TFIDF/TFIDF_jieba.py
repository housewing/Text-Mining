#encoding=utf-8
import pyodbc
import jieba
import jieba.analyse
import pandas as pd
from pandas import DataFrame
from collections import defaultdict
from operator import itemgetter
import re
import math

def read_access(str):
    database = '../Data/ke2016_sample_data.accdb'
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + database + ';'
    )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    file_list = [row.content for row in crsr.execute("SELECT * FROM ke2016_sample_news WHERE section like '%s' OR section like '%s'" % (str[0], str[1]))]
    return file_list

def write_excel(word_tfidf_sort, filename, sheet):
    print('----- Write Excel -----')
    df = pd.DataFrame(list(word_tfidf_sort),
                      columns=['Key', 'TFIDF'])
    # print('df :\n', df)

    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet, index=False)
    writer.save()

def cal_term_frequency(line, word_tf):
    doc_word = defaultdict(list)  # record a doc with what words
    for tmp_line in line:
        for seg in jieba.cut(tmp_line, cut_all=False):
            word_tf[seg] += 1
            doc_word[seg] = 1
    return doc_word

def create_index(data):
    index = defaultdict(list)
    for i, tokens in enumerate(data):
        for token in tokens:
            index[token].append(i)
    return index

def main():
    jieba.set_dictionary('dict.txt.big')  # for Chinese(Traditional)
    str = ['%財經%', '%產經%']
    file_list = read_access(str)
    print('All of file :', len(file_list))

    doc_word = []
    word_tf = defaultdict(int)
    line_list = [[line for line in re.split('，|。| |、|<BR>●|<BR>|：', file)] for file in file_list]
    for line in line_list:
        doc_word.append(cal_term_frequency(line, word_tf))

    print('All of ngram with term frequency:', len(word_tf))

    doc_word_index = create_index(doc_word)
    print('----- Finish Inverted Index ------')
    # print(doc_word_index.keys())
    # print(doc_word_index['微軟'])

    word_tfidf = defaultdict()
    for word in word_tf:
        file_size = len(file_list)
        tf = word_tf.get(word)
        df = len(doc_word_index[word])
        if tf > 5 & df < file_size * 0.75:
            # print(tf, ' ', len(doc_word_index[word]))
            tfidf = math.log(tf) * (math.log(file_size / df) + 1)
            if tfidf > 25:
                word_tfidf[word] = tfidf
                # print(word, ' ', tfidf)

    print('----- Finish calculate TFIDF ------')
    # print('length of word_tfidf :', len(word_tfidf))

    word_tfidf_sort = sorted(word_tfidf.items(), key=itemgetter(1), reverse=True)
    write_excel(word_tfidf_sort, 'Keyword_jieba.xlsx', 'Sheet1')
    # for word in word_tfidf_sort:
    #     print(word[0], ' ', word[1])

    #----- Use jieba library to extract keyword -----
    jieba_word = defaultdict(int)
    jieba_value = defaultdict(float)
    for file in file_list:
        for keyword, value in jieba.analyse.extract_tags(file, withWeight=True):
            jieba_word[keyword] += 1
            jieba_value[keyword] += value
            # print('%s %s' % (keyword, value))
    print('length of jieba', len(jieba_word))

    jieba_keyword = defaultdict(float)
    for word in jieba_word:
        jieba_keyword[word] += (jieba_value[word] / jieba_word.get(word))

    jieba_sort = sorted(jieba_keyword.items(), key=itemgetter(1), reverse=True)
    for word in jieba_sort[0:200]:
        print(word[0], ' ', word[1])

if __name__ == '__main__':
    main()