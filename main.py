import xlrd
import mysql as ms

#设置路径
path = '/Users/joey/Desktop/idz_pl_contract.xls'

#打开EXCEL文件
data = xlrd.open_workbook(path)

#获取sheet页个数
sheetno = len(data.sheets())

#调用函数
ms.mysqlMD5(sheetno,path)