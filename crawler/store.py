import xlwt

book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet("my_sheet")


def save_data_to_excel(data):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet("my_sheet")
    sheet.write(0, 0, '标题')
    sheet.write(0, 1, '来源')
    sheet.write(0, 2, '时间')
# a=3
# b=0
# try:
#    print(5/0)
# except ZeroDivisionError:
#     print("除数不能为0")
#

try:
    print(5/2)
    file = open('dd')
except FileNotFoundError:# 可能产生的异常类型（这里可以填写多个异常，逗号隔开）:
    print(FileNotFoundError)#（打印异常信息，通知用户或者其他的处理）
    file = open('abc.txt')
finally:
    print('都会执行')
file.close()