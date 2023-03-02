#导入相关库
import os
import xlrd

path = '/Users/joey/Desktop/idz_pl_contract.xls'
data = xlrd.open_workbook(path)

table = data.sheets()[0]
rows = table.nrows

#获取文件名称
fn = path.split('/')[-1:]

#切分出表名
tablename = fn[0][0:-4]

#生成相关脚本文件
#给文件命名
txtfn = tablename + '_md5'
sqlfile = open(txtfn,'a')

#生成insert语句
sqlfile.writelines("insert overwrite table udm_idz." + tablename + "_md5 \nselect\n")


#拼接字段
ziduan = ''
for row in range(1,rows):
    columns = str(table[row][0])
    comment = str(table[row][1])
    addflag = str(table[row][2])

    #判断是否为新增字段
    if addflag[6:-1] != "是":
        ziduan =  ziduan + columns[6:-1] + ',        --' + comment[6:-1] + '\n'
    else:
        continue

#拼接字段
sqlfile.writelines(ziduan + "MD5(CONCAT_WS(','\n")

#拼接MD5计算字段
md5zd = ''
for row in range(1,rows):
    columns = str(table[row][0])

    #判断是否为不需要计算的字段
    if columns[-5:-1] != "_std" \
            and columns[6:-1].lower() != "log_id" \
            and columns[6:-1].lower() != "createtime" \
            and columns[6:-1].lower() != "updatetime" \
            and columns[6:-1].lower() != "isvalid" :
        md5zd = md5zd + ",NVL(CAST(" + columns[6:-1] + " AS string),'-|=')\n"
    else:
        continue

sqlfile.writelines(md5zd + ')) AS md5str\n')

#取新增字段
addzd = ''
for row in range(1,rows):
    columns = str(table[row][0])
    comment = str(table[row][1])
    addflag = str(table[row][2])

    #判断是否为新增字段
    if addflag[6:-1] == "是":
        addzd =  addzd + "," + columns[6:-1] + '        --' + comment[6:-1] + '\n'
    else:
        continue

sqlfile.writelines(addzd)

#取分区字段
partition = ''
for row in range(1,rows):
    columns = str(table[row][3])
    values = str(table[row][4])

    #获取分区字段
    if columns != "empty:''":
        partition =  partition + "," + values[6:-1] + " as " + columns[6:-1] + "\n"
    else:
        continue

sqlfile.writelines(partition)

#取系统分区字段
sourceid = ''
for row in range(1,rows):
    columns = str(table[row][3])
    values = str(table[row][4])
    comment = str(table[row][5])

    #获取分区字段
    if comment[6:-1] == "系统分区":
        sourceid =  sourceid + columns[6:-1] + " = " + values[6:-1]
    else:
        continue

sqlfile.writelines("from udm_idz." + tablename + "_md5 where " + sourceid)