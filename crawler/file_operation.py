# from openpyxl import Workbook
# wb = Workbook()
#
# # grab the active worksheet
# ws = wb.active
#
# ws['A1'] = '列1'
# ws['B1'] = '列1'
# ws['C1'] = '列1'
# # Rows can also be appended
# ws.append(['python', 'js', 'java'])
# ws.append(['sql', 'C++', 'C#'])
# wb.save(r"sample.xlsx")

file = open('abc123.txt', 'w')
file.write("first line")
file.write("second line")
file.write("third line")
file.close()
