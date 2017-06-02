import pyodbc
import re
from collections import  defaultdict #dictionary method three
from operator import itemgetter # sort dictionart value

def read_access(str):
    database = '../Data/ke2016_sample_data.accdb'
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + database + ';'
    )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()
    file_list = [row.content for row in crsr.execute("SELECT * FROM ke2016_sample_news WHERE section like '%s'" % (str))]
    return file_list

def write_file(word_tf, filename, threshold):
    file = open(filename, 'w', encoding='UTF-8')
    for word in word_tf:
        if word_tf.get(word) > threshold: #tf greater than threhold
            file.write('%s %s\n' % (word, word_tf.get(word)))
    file.close()

def write_sort_file(word_tf_sort, filename, threshold):
    file = open(filename, 'w', encoding='UTF-8')
    for word in word_tf_sort:
        if word[1] > threshold: #tf greater than threhold
            file.write('%s %s\n' % (word[0], word[1]))
    file.close()

def ngrams(line_list, n):
    ngrams = []
    for i in range(len(line_list) - ( n - 1)):
        ngrams.append(line_list[i : i + n])
    return ngrams

def cal_term_frequency(tmp_line, word_tf):
    # start to count term frequency
    # #method one
    # word_tf = {}
    # for i in range(2, len(tmp_line) + 1 if len(tmp_line) < 9 else 9):
    #     n = ngrams(tmp_line, i)
    #     print(n)
    #
    #     for word in n:
    #         try:
    #             word_tf[word] +=1
    #         except KeyError:
    #             word_tf[word] = 1
    #
    # print('length:', len(word_tf))
    # print(word_tf)

    # #method two
    # word_tf = {}
    # for i in range(2, len(tmp_line) + 1 if len(tmp_line) < 9 else 9):
    #     n = ngrams(tmp_line, i)
    #
    #     for word in n:
    #         previous = word_tf.get(word, 0)
    #         word_tf[word] = previous + 1
    #
    # print('length:', len(word_tf))
    # print(word_tf)

    # method three --- need to import defaultdict module
    # word_tf = defaultdict(int)  # define before outer for loop
    for i in range(2, len(tmp_line) + 1 if len(tmp_line) < 9 else 9):
        n = ngrams(tmp_line, i)

        for word in n:
            word_tf[word] += 1

def main():
    str = '%財經%'
    file_list = read_access(str)
    print('All of file :', len(file_list))

    word_tf = defaultdict(int)
    line_list = [[line for line in re.split('，|。| |、', file)] for file in file_list]
    for line in line_list:
        for tmp_line in line:
            cal_term_frequency(tmp_line, word_tf)

    write_file(word_tf, 'output.txt', 3) #for original word_tf
    print('All of ngram with term frequency:', len(word_tf))

    word_tf_sort = sorted(word_tf.items(), key = itemgetter(1), reverse = True)
    write_sort_file(word_tf_sort, 'output_sort.txt', 3) #for word_tf sorted by value

if __name__ == '__main__':
    main()