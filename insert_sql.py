import xlrd

def insert_sql(num,path):

    #获取表名
    fn = path.split('/')[-1:]
    tablename = fn[0][0:-4]

    data = xlrd.open_workbook(path)
    table = data.sheets()[num]
    rows = table.nrows

    #拼接字段
    ziduan = ''
    for row in range(1,rows):
        columns = str(table[row][0])
        comment = str(table[row][1])
        addflag = str(table[row][3])

        #判断是否为新增字段
        if addflag[6:-1] != "是" and row == 1:
            ziduan =  ziduan + columns[6:-1]
        elif addflag[6:-1] != "是":
            ziduan = ziduan + ',' + columns[6:-1]
        else:
            continue

    addzd = ''
    count = 0
    for row in range(1,rows):
        columns = str(table[row][0])
        comment = str(table[row][1])
        addflag = str(table[row][3])

        #判断是否为新增字段
        if addflag[6:-1] == "是":
            count = count + 1
            if count == 1:
                addzd =  addzd + columns[6:-1]
            else:
                addzd = addzd + ',' + columns[6:-1]
        else:
            continue

     # 取分区字段
    partition = ''
    countp = 0
    for row in range(1, rows):
        columns = str(table[row][5])

        # 获取分区字段
        if columns != "empty:''" :
            countp = countp +1
            if countp == 1:
                partition = partition + columns[6:-1]
            else:
                partition = partition + ',' + columns[6:-1]
        else:
            continue

    #获取主键
    pk = ''
    countpk = 0
    for row in range(1, rows):
        columns = str(table[row][0])
        pkflag = str(table[row][4])

        if pkflag[6:-1] == "是":
            countpk = countpk + 1
            if countpk == 1:
                pk = pk + columns[6:-1]
            else :
                pk = pk + "," + columns[6:-1]
        else:
            continue

    return tablename,ziduan,addzd,pk,partition