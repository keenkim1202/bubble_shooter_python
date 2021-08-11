# !/usr/lcoal/bin/python
# -*- coding:  utf-8 -*-

# Àç±Í È£Ãâ
# for i in range(1, 6):
#     print(i)

#     if i == 5:
#         print("end num.")

def count_1():
    print(1)
    count_2()
    print("1 end")

def count_2():
    print(2)
    count_3()
    print("2 end")

def count_3():
    print(3)
    count_4()
    print("3 end")

def count_4():
    print(4)
    count_5()
    print("4 end")

def count_5():
    print(5)
    print("end num>..")
    print("5 end")

# count_1()

def count(num):
    print(num)

    if num == 5:
        print("end count.")
    else:
        count(num + 1)
        print(num, "end")
# count(1)

def factorial(n):
    if n > 1:
        return n * factorial(n -1)
    else:
        return 1

result = factorial(4)
print(result) # 24