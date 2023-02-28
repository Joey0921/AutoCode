#导入相关库
import os
#import xlrd
#
#path = '/Users/joey/Desktop/idz_pl_contract.xls'
#data = xlrd.open_workbook(path)
#
#table = data.sheets()[0]
#rows = table.nrows
#columns = table.ncols
#
#for i in range(columns):
#    print(table.)
import pandas as pd
df = pd.read_excel('/Users/joey/Desktop/idz_pl_contract.xls')
data=df.values
print("获取到所有的值:\n{}".format(data))




