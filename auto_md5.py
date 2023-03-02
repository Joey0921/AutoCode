#导入相关库
import xlrd
def auto_md5(num,path):
    data = xlrd.open_workbook(path)

    for sn in range(0,num):
        table = data.sheets()[sn]
        rows = table.nrows

        #获取文件名称
        fn = path.split('/')[-1:]

        #切分出表名
        tablename = fn[0][0:-4]

        #生成相关脚本文件
        #给文件命名
        txtfn = tablename + '_md5'
        sqlfile = open(txtfn,'a')

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

        #拼接字段
        sqlfile.writelines("insert overwrite table udm_idz." + tablename + "_md5 \nselect\n"
                           + ziduan + "MD5(CONCAT_WS(','\n"
                           + md5zd + ')) AS md5str\n'
                           + addzd
                           + partition
                           + "from udm_idz." + tablename + "_md5 where " + sourceid + "\n"
                           )