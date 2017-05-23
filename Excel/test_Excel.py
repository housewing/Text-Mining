import pandas as pd # need to install pandas, openpyxl
from pandas import DataFrame
from collections import  defaultdict

def getNGrams(line_list, n):
    ngrams = []
    for i in range(len(line_list) - ( n - 1)):
        ngrams.append(line_list[i : i + n])
    return ngrams

def calTermFrequency(tmp_line, word_tf):
    for i in range(2, len(tmp_line) + 1 if len(tmp_line) < 9 else 9):
        for word in getNGrams(tmp_line, i):
            word_tf[word] += 1

def main():
    sheet = 'Sheet1'
    filename = 'out.xlsx'

    str = '吃葡萄不吐葡萄皮，不吃葡萄倒吐葡萄皮'
    str_list = [s for s in str.split('，')]
    print('str_list :', str_list)

    word_tf = defaultdict(int)
    for str in str_list:
        calTermFrequency(str, word_tf)
    print('word_tf :', word_tf)

    print('----- Write Excel -----')
    df = pd.DataFrame(list(word_tf.items()),
                      columns=['Key', 'TFIDF'])
    # print('df :\n', df)

    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, sheet, index=False)
    writer.save()

    print('----- Read Excel -----')
    df = pd.read_excel(filename, header=[0], index_col=[0,1], sheetname=sheet)
    print('First Columns :')
    for word in df.index:
        print(word, ' ', word[0], ' ', word[1])

if __name__ == '__main__':
    main()

#http://pandas.pydata.org/pandas-docs/stable/dsintro.html.
#https://stackoverflow.com/questions/18837262/convert-python-dict-into-a-dataframe
#http://pandas.pydata.org/pandas-docs/version/0.20/generated/pandas.read_excel.html