import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="attendance"
)

cur = mydb.cursor()
#cur.execute("show tables;")
cur.execute("select * from stu_info")

myresult = cur.fetchall()

for x in myresult:
  print(x)