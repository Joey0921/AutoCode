import pymysql as pysql

db = pysql.connect(host="localhost",user="root",password="12345678")

cursor = db.cursor()

createdatabase = "create database if not exists autocoding;"

cursor.execute(createdatabase)
