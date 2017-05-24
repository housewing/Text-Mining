import pyodbc
import re

import pandas as pd # need to install pandas, openpyxl
from pandas import DataFrame

from math import log
from collections import  defaultdict #dictionary method three
from operator import itemgetter # sort dictionart value

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

def writeExcel(long_term_word, filename, sheet):
    df = pd.DataFrame(list(long_term_word),
                      columns=['Key', 'TFIDF'])

    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet, index=False)
    writer.save()

def getNGrams(line_list, n):
    ngrams = []
    for i in range(len(line_list) - ( n - 1)):
        ngrams.append(line_list[i : i + n])
    return ngrams

def calTermFrequency(line, word_tf):
    doc_word = defaultdict(list) #record a doc with what words
    for tmp_line in line:
        for i in range(2, len(tmp_line) + 1 if len(tmp_line) < 9 else 9):
            for word in getNGrams(tmp_line, i):
                word_tf[word] += 1
                doc_word[word] = 1
    return doc_word

def create_index(data):
    index = defaultdict(list)
    for i, tokens in enumerate(data):
        for token in tokens:
            index[token].append(i)
    return index

def getLongTermWordBySameValue(word_tfidf, tfidf_value):
    long_term_word_by_same_value = defaultdict()
    for value in tfidf_value:
        tmp_list = []
        for word in word_tfidf:
            if value == word_tfidf.get(word):
                tmp_list.append(word)

        longest_word = max(tmp_list, key=len)
        for word in tmp_list:
            if longest_word.__str__().find(word) == -1:
                long_term_word_by_same_value[word] = value

        long_term_word_by_same_value[longest_word] = value

    word_tfidf_sort = sorted(long_term_word_by_same_value.items(), key=itemgetter(1), reverse=True)
    # word_tfidf_sort = sorted(long_term_word_by_same_value.items(), key=lambda  x:(x[1], len(x[0])), reverse=True)
    return word_tfidf_sort

def main():
    str = ['%財經%', '%產經%']
    file_list = readAccess(str)
    print('All of file :', len(file_list))

    doc_word = []
    word_tf = defaultdict(int)
    line_list = [[line for line in re.split('，|。| |、|<BR>●|<BR>|：|-', file)] for file in file_list]
    for line in line_list:
        doc_word.append(calTermFrequency(line, word_tf))

    print('All of ngram with term frequency:', len(word_tf))

    doc_word_index = create_index(doc_word)
    print('----- Finish Inverted Index ------')
    # print(doc_word_index.keys())

    word_tfidf = defaultdict()
    tfidf_value = defaultdict()
    for word in word_tf:
        file_size = len(file_list)
        tf = word_tf.get(word)
        df = len(doc_word_index[word])
        if tf > 5 & df < file_size * 0.75:
            # print(tf, ' ', len(doc_word_index[word]))
            tfidf = log(tf) * (log(file_size / df) + 1)
            if tfidf > 25:
                word_tfidf[word] = tfidf
                tfidf_value[tfidf] = 1
                # print(word, ' ', tfidf)

    print('----- Finish calculate TFIDF ------')
    print('length of word_tfidf :', len(word_tfidf))
    print('length of tfidf_value :', len(tfidf_value))

    long_term_word = getLongTermWordBySameValue(word_tfidf, tfidf_value)

    print('length of long-term word :', len(long_term_word))
    for word in long_term_word:
        print(word[0], ' ', word[1])

    writeExcel(long_term_word, 'Keyword_myself.xlsx', 'Sheet1')

if __name__ == '__main__':
    main()