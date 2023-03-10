#导入相关库
import time
import xlrd
import os

def auto_incr_md5(num,path):
    data = xlrd.open_workbook(path)

    #for sn in range(0,num):
    table = data.sheets()[num]
    rows = table.nrows

    #获取日期
    dt = time.strftime("%Y/%m/%d",time.localtime())
    #获取文件名称
    fn = path.split('/')[-1:]

    #切分出表名
    tablename = fn[0][0:-4]

    #生成相关脚本文件
    #给文件命名
    #判断是否有系统来源
    #取系统分区字段
    source = ''
    sourceid = ''
    for row in range(1, rows):
        columns = str(table[row][5])
        values = str(table[row][6])
        comment = str(table[row][7])

        # 获取分区字段
        if comment[6:-1] == "系统分区":
            sourceid = sourceid + columns[6:-1] + " = \'" + values[6:-1] + "\'"
            source = source + values[6:-1]
        else:
            continue
    if source != '':
        txtfn = tablename + '_incr_md5_' +source.lower() + '.xml'
    else:
        txtfn = tablename + '_incr_md5.xml'

    if os.path.exists(txtfn) == False:
        sqlfile = open(txtfn,'a')

        #拼接字段
        ziduan = ''
        for row in range(1,rows):
            columns = str(table[row][0])
            comment = str(table[row][1])
            addflag = str(table[row][3])

            #判断是否为新增字段
            if addflag[6:-1] != "是":
                ziduan =  ziduan + columns[6:-1] + ',        --' + comment[6:-1] + '\n'
            else:
                continue

        #拼接MD5计算字段
        md5zd = ''
        for row in range(1,rows):
            columns = str(table[row][0])
            businessflag = str(table[row][2])

            #判断是否为不需要计算的字段
            if businessflag[6:-1] != "否":
                md5zd = md5zd + ",NVL(CAST(" + columns[6:-1] + " AS string),'-|=')\n"
            else:
                continue

        #取新增字段
        addzd = ''
        for row in range(1,rows):
            columns = str(table[row][0])
            comment = str(table[row][1])
            addflag = str(table[row][3])

            #判断是否为新增字段
            if addflag[6:-1] == "是":
                addzd =  addzd + "," + columns[6:-1] + '        --' + comment[6:-1] + '\n'
            else:
                continue

        #取分区字段
        partition = ''
        for row in range(1,rows):
            columns = str(table[row][5])
            values = str(table[row][6])
            comment = str(table[row][7])
            #获取分区字段
            if columns != "empty:''" and comment[6:-1] == "系统分区":
                partition = partition + ",\'" + values[6:-1] + "\' as " + columns[6:-1] + "\n"
            elif columns != "empty:''":
                partition = partition + "," + values[6:-1] + " as " + columns[6:-1] + "\n"
            else:
                continue

        xmldesc1 = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <root>"
        <tasklist>
        <task database="udm_idz" author=\"""" + str(table[1][8])[6:-1] + """\" createTime=\"""" + str(dt) + """\" updater=" " updateTime=" ">
            <sqllist>
                <sql index="1" registerF1ag="0" tableName="" sinkFlag="0" saveMode="" persistF1ag="0" persistlevel="">
                    <desc><![CDATA[ 落地当天的MD5全量备份表 ]]></desc>
                    <context>
                    <![CDATA[\n"""

        #拼接字段
        sqlfile.writelines(xmldesc1 + "insert overwrite table udm_idz." + tablename + "_md5 \nselect\n"
                           + ziduan + "MD5(CONCAT_WS(','\n"
                           + md5zd + ')) AS md5str\n'
                           + addzd
                           + partition
                           + "from udm_idz." + tablename + "_md5 where " + sourceid + "\n"
                           )

        # 生成相关脚本文件
        # 给文件命名
        # 判断是否有系统来源
        # 取系统分区字段
        source = ''
        sourceid = ''
        for row in range(1, rows):
            columns = str(table[row][5])
            values = str(table[row][6])
            comment = str(table[row][7])

            # 获取分区字段
            if comment[6:-1] == "系统分区":
                sourceid = sourceid + columns[6:-1] + " = \'" + values[6:-1] + "\'"
                source = source + values[6:-1]
            else:
                continue

        # 拼接字段
        iuziduan = ''
        for row in range(1, rows):
            columns = str(table[row][0])
            comment = str(table[row][1])
            addflag = str(table[row][3])

            # 判断是否为新增字段
            if addflag[6:-1] != "是" and row == 1:
                iuziduan = iuziduan + "today." + columns[6:-1] + '        --' + comment[6:-1] + '\n'
            elif addflag[6:-1] != "是":
                iuziduan = iuziduan + ",today." + columns[6:-1] + '        --' + comment[6:-1] + '\n'
            else:
                continue

        # 取新增字段
        iuaddzd = ''
        for row in range(1, rows):
            columns = str(table[row][0])
            comment = str(table[row][1])
            addflag = str(table[row][3])
            # 判断是否为新增字段
            if addflag[6:-1] == "是":
                iuaddzd = iuaddzd + ",today." + columns[6:-1] + '        --' + comment[6:-1] + '\n'
            else:
                continue

        # 拼接字段
        dziduan = ''
        for row in range(1, rows):
            columns = str(table[row][0])
            comment = str(table[row][1])
            addflag = str(table[row][3])

            # 判断是否为新增字段
            if addflag[6:-1] != "是" and row == 1:
                dziduan = dziduan + "yesterday." + columns[6:-1] + '        --' + comment[6:-1] + '\n'
            elif addflag[6:-1] != "是":
                dziduan = dziduan + ",yesterday." + columns[6:-1] + '        --' + comment[6:-1] + '\n'
            else:
                continue

        # 取新增字段
        daddzd = ''
        for row in range(1, rows):
            columns = str(table[row][0])
            comment = str(table[row][1])
            addflag = str(table[row][3])
            # 判断是否为新增字段
            if addflag[6:-1] == "是":
                daddzd = daddzd + ",yesterday." + columns[6:-1] + '        --' + comment[6:-1] + '\n'
            else:
                continue

        # 取分区字段
        partition = ''
        for row in range(1, rows):
            columns = str(table[row][5])
            values = str(table[row][6])
            comment = str(table[row][7])
            # 获取分区字段
            if columns != "empty:''" and comment[6:-1] == "系统分区":
                partition = partition + ",\'" + values[6:-1] + "\' as " + columns[6:-1] + "\n"
            elif columns != "empty:''":
                partition = partition + "," + values[6:-1] + " as " + columns[6:-1] + "\n"
            else:
                continue

        # 获取主键
        pk = ''
        pkjoin = ''
        pk1 = ''
        count = 0
        for row in range(1, rows):
            columns = str(table[row][0])
            pkflag = str(table[row][4])

            if pkflag[6:-1] == "是":
                count = count + 1
                if count == 1:
                    pk = pk + columns[6:-1]
                    pkjoin = pkjoin + "today." + columns[6:-1] + " = yesterday." + columns[6:-1] + "\n"
                    pk1 = pk1 + columns[6:-1]
                else:
                    pk = pk + "," + columns[6:-1]
                    pkjoin = pkjoin + "and today." + columns[6:-1] + " = yesterday." + columns[6:-1] + "\n"
            else:
                continue

        # 拼接新增数据逻辑
        incr = "insert overwrite table udm_idz." + tablename + "_incr_md5 \nselect\n" \
               + iuziduan + ",today.md5str\n,'I' as idz_datatype\n" \
               + iuaddzd \
               + partition \
               + "from udm_idz." + tablename + "_md5 today \n" \
               + "left join (select " \
               + pk + " from udm_idz." \
               + tablename + "_md5 where " \
               + sourceid \
               + " and dt = date_sub(FROM_UNIXTIME(UNIX_TIMESTAMP()),1)) yesterday \non " \
               + pkjoin \
               + "where today." + sourceid + "\n" \
               + "and today.dt = date_format(current_timestamp,'yyyy-MM-dd')\n" \
               + "and yesterday." + pk1 + " is null\nunion all\n"

        update = "select \n" \
                 + iuziduan + ",today.md5str\n,'U' as idz_datatype\n" \
                 + iuaddzd \
                 + partition \
                 + "from udm_idz." + tablename + "_md5 today \n" \
                 + "inner join (select " \
                 + pk + ",md5str from udm_idz." \
                 + tablename + "_md5 where " \
                 + sourceid \
                 + " and dt = date_sub(FROM_UNIXTIME(UNIX_TIMESTAMP()),1)) yesterday \non " \
                 + pkjoin \
                 + "where today." + sourceid + "\n" \
                 + "and today.dt = date_format(current_timestamp,'yyyy-MM-dd')\n" \
                 + "and today.md5str <> yesterday.md5str\nunion all\n"

        delete = "select \n" \
                 + dziduan + ",yesterday.md5str\n,'D' as idz_datatype\n" \
                 + daddzd \
                 + partition \
                 + "from udm_idz." + tablename + "_md5 yesterday \n" \
                 + "left join (select " \
                 + pk + " from udm_idz." \
                 + tablename + "_md5 where " \
                 + sourceid \
                 + " and dt = date_format(current_timestamp,'yyyy-MM-dd')) today \non " \
                 + pkjoin \
                 + "where yesterday." + sourceid + "\n" \
                 + "and yesterday.dt = date_sub(FROM_UNIXTIME(UNIX_TIMESTAMP()),1)\n" \
                 + "and yesterday." + pk1 + " is null"

        xmldesc2 = """]]>
                        </context>
                    </sql>
                    <sql index="2" registerF1ag="0" tableName="" sinkFlag="0" saveMode="" persistF1ag="0" persistlevel="">
                        <desc><![CDATA[ 计算当天的增量数据并落地至增量表 ]]></desc>
                        <context>
                        <![CDATA[\n"""

        xmldesc3 = """]]>
                          </context>
                          </sql>
                    </sqllist>
                </task>
            </tasklist>
            </root>"""
        sqlfile.writelines(xmldesc2 + incr + update + delete + "\n" + xmldesc3)
        sqlfile.close()
