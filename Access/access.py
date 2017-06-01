import pyodbc
import os
import sys

def main():
    str = '%財經%'
    database = '../Data/ke2016_sample_data.accdb'
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + database + ';'
    )
    cnxn = pyodbc.connect(conn_str)
    crsr = cnxn.cursor()

    # #method one
    # tmp_file = []
    # for row in crsr.execute("SELECT * FROM ke2016_sample_news WHERE section like '%s'" % (str)):
    #     tmp_file.append(row.content)
    #method two
    tmp_file = [row.content for row in crsr.execute("SELECT * FROM ke2016_sample_news WHERE section like '%s'" % (str))]
    print('Number of file :', len(tmp_file))
    print(tmp_file[0])

if __name__ == '__main__':
    main()

# https://github.com/mkleehammer/pyodbc/tree/master/tests3
