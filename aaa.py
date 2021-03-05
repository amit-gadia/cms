from flask import *
import mysql.connector
ab=mysql.connector.connect(host="localhost",user="root",password="Root@123",database="abc")
crs=ab.cursor(buffered=True)
brname=input()
sql2="INSERT INTO users(name) VALUES(%s);"
val = ("Michelle",)
crs.execute(sql2,val)
ab.commit()
