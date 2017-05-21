import os
import sys

def readfile(filename):
    file = open(filename, 'r', encoding='UTF-8')
    try:
        # method one
        # tmp_number = []
        # for line in file:
        #     tmp_number.append([int(data) for data in line.split()])
        # ---------------
        #method two
        tmp_number = [[int(data) for data in line.split()] for line in file]
    except:
        print("read file error")
    finally:
        file.close()

    # output is two dimension array
    # print(len(tmp_number[0]))

    # convert to one dimension array
    # method one
    number = [col for row in tmp_number for col in row]
    # ---------------
    # # method two
    # number = []
    # for row in tmp_number:
    #     for col in row:
    #         number.append(col)

    # print(number)
    return number

def writeFile(number):
    filename = 'output.txt'
    with open(filename, 'w') as file:
        file.write('{}'.format(number))
		
def main():
    def selection(number):
        # 找出未排序中最小值
        def min(m, j):
            if j == len(number):
                # print("one")
                return m
            elif number[j] < number[m]:
                # print("two ", j, " ", j + 1)
                return min(j, j + 1)
            else:
                # print("three", m, " ", j + 1)
                return min(m, j + 1)

        for i in range(0, len(number)):
            # print("i : ", i, " , i + 1 : ", i + 1)
            m = min(i, i + 1)
            if i != m:
                # print("before : ", number[i], " ", number[i + 1])
                number[i], number[m] = number[m], number[i]
                # print("after : ", number[i], " ", number[i + 1])

    number = readfile('../Data/num.txt')
    print("before sort : ", number)

    selection(number)
    print("after sort : ", number)
	
	writeFile(number)

if __name__=='__main__':
    main()