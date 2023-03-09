import xlrd

def concatColumns(sno,num,path):
    data = xlrd.open_workbook(path)

    table = data.sheets()[sno]
    # 拼接字段
    ziduan = ''
    for row in range(1, num):
        columns = str(table[row][0])

        if row == 1:
            ziduan = ziduan + columns[6:-1]
        else:
            ziduan = ziduan + ',' + columns[6:-1]

    return ziduan