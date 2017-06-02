import pyodbc
import numpy as np
import pandas as pd
from pandas import DataFrame
from collections import defaultdict
from operator import itemgetter
import math
import re

class_list = ['財經', '體育', '政治', '兩岸', '娛樂', '社會', '家庭']

class token:
    def __init__(self, id, title, section, content):
        self.id = id
        self.title = title
        self.section = section
        self.content = content

def change_class(x):
    return {'財經' : '財經', '體育' : '體育', '運動' : '體育', '政治' : '政治', '兩岸' : '兩岸', '娛樂' : '娛樂', '影劇' : '娛樂', '社會' : '社會', '家庭' : '家庭'}[x]

def read_access(database):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + database + ';'
    )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    file_list = []
    for row in crsr.execute("SELECT * FROM ke2016_sample_news"):
        file_list.append(token(row.id, row.title, change_class(row.section[:2]), row.content))
    return file_list

def read_excel(filename, sheet):
    key_list = defaultdict(int)
    df = pd.read_excel(filename, header=[0], index_col=[0], sheetname=sheet)
    count = 0
    for word in df.index:
        key_list[word] = count
        count += 1
    return key_list

def ngrams(line_list, n):
    ngrams = []
    for i in range(len(line_list) - ( n - 1)):
        ngrams.append(line_list[i : i + n])
    return ngrams

def tag_doc_keyword(line, key_list):
    doc_word_tf = defaultdict(int)
    for tmp_line in line:
        for i in range(2, len(tmp_line) + 1 if len(tmp_line) < 9 else 9):
            for word in ngrams(tmp_line, i):
                if key_list.get(word) != None:
                    doc_word_tf[word] += 1
    return doc_word_tf

def create_tf_matrix(file_list, col, doc_word_tf, key_list):
    tf_matrix = np.zeros((len(file_list), col))  # initial matrix
    for i in range(0, len(tf_matrix)):
        doc_word = doc_word_tf[i]
        for word in doc_word:
            sub_col = key_list.get(word)
            tf_matrix[i][sub_col] = doc_word.get(word)
        tf_matrix[i][(col - 1)] = class_list.index(file_list[i].section) # record class

    # for i in range(len(tf_matrix[0])):
    #     if tf_matrix[0][i] != 0:
    #         print(i, ' ', tf_matrix[0][i])
    return tf_matrix

def create_probability_matrix(tf_matrix, key_len, file_len):
    class_len = len(class_list)
    sum_matrix = np.zeros((class_len, key_len + 1))  # initial  matrix
    for matrix in tf_matrix:
        num_class = int(matrix[key_len])
        np.add(sum_matrix[num_class][0:key_len], matrix[0:key_len], sum_matrix[num_class][0:key_len])
        np.add(sum_matrix[num_class][key_len:key_len + 1], np.ones(1),sum_matrix[num_class][key_len:key_len + 1])
    # print(sum_matrix)

    # for m in sum_matrix:
    #     print(m[len(key_list)])

    probability_matrix = np.zeros((class_len, key_len + 1))
    for i in range(0, class_len):
        sum_tf = sum(sum_matrix[i][0:key_len]) + key_len
        # np.add(sum_matrix[i][0:key_len], np.log(np.divide(np.add(sum_matrix[i][0:key_len], np.ones(1)), np.ones(1) * sum_tf)),
        #        sum_matrix[i][0:key_len])
        # np.add(probability_matrix[i][key_len:key_len + 1], np.log(sum_matrix[i][key_len: key_len + 1]) / file_len,
        #        probability_matrix[i][key_len:key_len + 1])
        for j in range(0, key_len):
            probability_matrix[i][j] = math.log((sum_matrix[i][j] + 1) / sum_tf)
        probability_matrix[i][key_len] = math.log(sum_matrix[i][key_len] / file_len)
    # print(probability_matrix)

    # for m in probability_matrix:
    #     print(m[key_len])
    return probability_matrix

def navieBayers(number, probability_matrix, tf_matrix, doc_word_tf, key_len, file_list):
    set_list = defaultdict(int)
    for i in range(0, len(class_list)):
        matrix = probability_matrix[i]
        s = sum(np.multiply(matrix[0:key_len], tf_matrix[number][0:key_len])) + matrix[key_len]
        set_list[class_list[i]] = s

    print(file_list[number].title, '     ', file_list[number].section, '\n', doc_word_tf[number])
    print(' ----- ***** ----- ', max(set_list.items(), key=itemgetter(1))[0], ' ', max(set_list.items(), key=itemgetter(1))[1])

def main():
    file_list = read_access('../Data/ke2016_sample_data.accdb')
    print('length of file :', len(file_list))
    # for file in file_list[0:5]:
    #     print('id :', file.id, ' title :', file.title, ' section :', file.section, ' number :', file.num)

    key_list = read_excel('../Data/keyword_2100.xlsx', 'Sheet1')
    print('length of keyword :', len(key_list))
    # for key in key_list:
    #     print(key, ' ', key_list.get(key))

    doc_word_tf = []
    line_list = [[line for line in re.split('，|。| |、|<BR>●|<BR>|：', file.content)] for file in file_list]
    for line in line_list:
        doc_word_tf.append(tag_doc_keyword(line, key_list))
    print('----- Finish Tag Doc -----')

    #create a tf matrix by numpy
    key_len = len(key_list)
    tf_matrix = create_tf_matrix(file_list, key_len + 1, doc_word_tf, key_list)
    print('----- Finish TF matrix ------')

    probability_matrix = create_probability_matrix(tf_matrix, key_len, len(file_list))
    print('----- Finish probability matrix ------')

    while True:
        number = int(input('Please input number ( 0 - 13801 ):')) #5000
        navieBayers(number, probability_matrix, tf_matrix, doc_word_tf, key_len, file_list)
        if(input('continue? (q to exit)') == 'q'):
            break

if __name__ == '__main__':
    main()