
import pymysql as pysql
#设置路径
path = '/Users/joey/Desktop/idz_pl_contract.xls'

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

selectsql = "select num, tablename, original_col, incr_col from autocoding.autocode_config where tablename = %s and valid_flag = '1'"
cur.execute(selectsql,(tablename))
result1 = cur.fetchone()
hiscol = result1[2] + ',' + result1[3]
list = hiscol.split(',')
length = len(list)
print(length)



