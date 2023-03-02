import auto_md5 as am
import auto_incr_md5 as aim
import xlrd

#设置路径
path = '/Users/joey/Desktop/idz_pl_contract.xls'

#打开EXCEL文件
data = xlrd.open_workbook(path)

#获取sheet页个数
sheetno = len(data.sheets())

#调用函数
am.autoMD5(sheetno,path)
aim.autoINCRMD5(sheetno,path)

