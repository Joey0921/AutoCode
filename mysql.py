import pymysql as pysql
import auto_incr_md5 as am
import insertSQL as iq
import concatColumns as cc

def mysqlMD5(num,path):
    #连接数据库
    db = pysql.connect(host="localhost",user="root",password="12345678")

    #创建游标
    cur = db.cursor()

    #获取表名
    fn = path.split('/')[-1:]
    tablename = fn[0][0:-4]

    #查询表是否存在
    isexist = "select count(1) from autocoding.autocode_config where tablename = %s"

    #执行SQL
    cur.execute(isexist,tablename)

    #获取结果
    result = cur.fetchone()

    for sn in range(0,num):
        #判断结果
        if result[0] == 0:
            am.autoMD5(sn,path)
            turple = iq.insertSQL(sn, path)
            if sn == 0:
                #插入语句
                insertsql = "insert into autocoding.autocode_config (num, tablename, original_col, incr_col, primary_key, partition_key, update_time, valid_flag) " \
                            "values (num,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP(),'1')"
                cur.execute(insertsql,(turple[0]
                           ,turple[1]
                           ,turple[2]
                           ,turple[3]
                           ,turple[4]))
                db.commit()
            else:
                continue
        else:
            selectsql = "select num, tablename, original_col, incr_col from autocoding.autocode_config where tablename = %s and valid_flag = '1'"
            cur.execute(selectsql,(tablename))
            result1 = cur.fetchone()
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
            #for sn in range(0,num):
            newcol = cc.concatColumns(sn,cn+1,path)
            if hiscol == newcol:
                am.autoMD5(sn, path)
                updatesql = "update autocoding.autocode_config set valid_flag = 0 where tablename = %s;"
                turple = iq.insertSQL(sn, path)
                # 插入语句
                if hiscol != turple[1] + ',' + turple[2] :
                    insertsql = "insert into autocoding.autocode_config (num, tablename, original_col, incr_col, primary_key, partition_key, update_time, valid_flag) " \
                            "values (num,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP(),'1')"
                    cur.execute(updatesql,(tablename))
                    db.commit()
                    cur.execute(insertsql, (turple[0]
                                        , turple[1]
                                        , turple[2]
                                        , turple[3]
                                        , turple[4]))
                    db.commit()
            else:
                print("您的第" + str(sn+1) +"个sheet页的表结构与上一个版本不一致，请检查！")
                print("旧版本的顺序是：" + hiscol)
                print("新版本的顺序是：" + newcol)
                yn = input('是否要进行替换？')
                if str(yn) == 'y':
                    am.autoMD5(sn, path)
                    updatesql = "update autocoding.autocode_config set valid_flag = 0 where tablename = %s;"
                    turple = iq.insertSQL(sn, path)
                    # 插入语句
                    if hiscol != turple[1] + ',' + turple[2]:
                        insertsql = "insert into autocoding.autocode_config (num, tablename, original_col, incr_col, primary_key, partition_key, update_time, valid_flag) " \
                                    "values (num,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP(),'1')"
                        cur.execute(updatesql, (tablename))
                        db.commit()
                        cur.execute(insertsql, (turple[0]
                                                , turple[1]
                                                , turple[2]
                                                , turple[3]
                                                , turple[4]))
                        db.commit()
                    else:
                        continue
                else:
                    print("您的第" + str(sn + 1) + "个sheet页的表结构与上一个版本不一致，请检查！")
                    print("旧版本的顺序是：" + hiscol)
                    print("新版本的顺序是：" + newcol)

    cur.close()
