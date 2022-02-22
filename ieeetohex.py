import pandas as pd
import binary_fractions

print("Press 1\nTo enter values manually\nPress 0 to\nTo take values from CSV file")
c = input()
e = ['Q1', 'Q2', 'Q3', 'Q4', 'q1', 'q2', 'q3', 'q4']
if c == '1':
    print("Enter the number of values")
    n = int(input())
    print("Enter the Q and value separated by comma")
    print("Example: Q1,0.177654")
    q = [input() for i in range(n)]
    Q = [k.split(",")[0] for k in q]
    q = [k.split(",")[1].replace("\n", "") for k in q]
    if not set(Q) <= set(e) or not all(i.isdigit() for i in q):
        print("Enter valid Q and values")
        quit()
else:
    input_file = open("Input_file.csv", 'r')
    q, Q = [], []
    for k in input_file:
        list_ = k.split(',')
        Q.append(list_[0])
        q.append(list_[1].replace('\n', ''))
    if not set(Q) <= set(e) or not all(i.isdigit() for i in q):
        print("Enter valid Q and values")
        quit()
    q, Q = q[1:], Q[1:]


df = pd.read_csv("D:\\Python\\OutputFile.csv")
for j, k in zip(q, Q):
    iee = ''
    sign = 0
    if float(j) < 0:
        sign = 1
    iee += str(sign)
    binary_n = str(binary_fractions.Binary(abs(float(j)))).replace('0b', '')
    if binary_n.find('.') < 0:
        binary_n += '.0'
    binary_n += '0' * (300 - len(binary_n))
    if binary_n.split(".")[0] == '0':
        exp = -(binary_n.split(".")[1].find('1') + 1)
    else:
        exp = len(binary_n.split(".")[0]) - 1
    iee += str(bin(127 + exp).zfill(10).replace("0b", ""))
    binary_n = binary_n.replace(".", "")
    if exp >= 0:
        mantissa = binary_n[1:24]
        if binary_n[24] == '1' and any(binary_n[24:]):
            mantissa = str(bin(int(binary_n[1:24], 2) + int('1', 2)))[2:].zfill(23)
        if binary_n[24] == '1':
            if mantissa[-1] == '1':
                mantissa = str(bin(int(binary_n[1:24], 2) + int('1', 2)))[2:].zfill(23)
    else:
        index = binary_n.find('1')
        mantissa = binary_n[index + 1: index + 24]
        if binary_n[index + 24] == '1' and any(binary_n[index + 24:]):
            mantissa = str(bin(int(binary_n[index + 1: + index + 24], 2) + int('1', 2)))[2:].zfill(23)
        if binary_n[index + 24] == '1':
            if mantissa[-1] == '1':
                mantissa = str(bin(int(binary_n[index + 1: + index + 24], 2) + int('1', 2)))[2:].zfill(23)
    iee += mantissa
    iee += '0' * (32 - len(iee))
    new_list = [iee[i:i + 4] for i in range(0, len(iee), 4)]
    hex_number = ""
    for i in new_list:
        hex_number += str(hex(int(i, 2))).replace("0x", "")
    print(j, hex_number.upper())
    df.loc[int(k[1])+1, 'Telecommand'] = '0XC418' + hex_number.upper() + '0000'
df.to_csv("D:\\Python\\OutputFile.csv", index=False)
