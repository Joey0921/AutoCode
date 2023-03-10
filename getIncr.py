import xlrd
import pymysql as pysql
import concatColumns as cc
def getIncr(num,path):
    #打开excel文件
    data = xlrd.open_workbook(path)

    # 连接数据库
    db = pysql.connect(host="localhost", user="root", password="12345678")

    # 创建游标
    cur = db.cursor()

    # 获取表名
    fn = path.split('/')[-1:]
    tablename = fn[0][0:-4]

    # 查询表是否存在
    isexist = "select count(1) from autocoding.autocode_config where tablename = %s"

    # 执行SQL
    cur.execute(isexist, tablename)

    # 获取结果
    result = cur.fetchone()


    selectsql = "select num, tablename, original_col, incr_col from autocoding.autocode_config where tablename = %s and valid_flag = '1'"

    cur.execute(selectsql,(tablename))
    result1 = cur.fetchone()

    for sn in range(0, num):
        #打开相关工作表
        table = data.sheets()[num]
        rows = table.nrows

        if result1[3] != '':
            hiscol = result1[2] + ',' + result1[3]
        else:
            hiscol = result1[2]
        list = hiscol.split(',')
        #判断长度，排除空字符串
        cn = 0
        for li in list:
            if li != '':
                cn = cn + 1
        newcol = cc.concatColumns(sn, cn + 1, path)

        #历史字段等于新字段
        if hiscol == newcol:
            #取新增字段
            for row in range(1, rows):
                columns = str(table[row][0])
                comment = str(table[row][1])
                addflag = str(table[row][3])

                # 判断是否为新增字段
                if addflag[6:-1] == "是":
                    addzd = addzd + "," + columns[6:-1] + '        --' + comment[6:-1] + '\n'
                else:
                    continue
