import os

try:
    print(5/0)
except ZeroDivisionError:
    print('0000000')
finally:
    print('都会执行')
print("ddd")


a_list = [1,2,3]
print(a_list)
for a_ in a_list:
    print(a_)
print(a_)
print(a_list)


print(os.listdir('/Users/chenjunbiao/python爬虫培训/crawler'))