import mysql.connector

mydb = mysql.connector.connect(
    host="pluto.cse.msstate.edu",
    user="pjb183",
    passwd="csePluto!"
)


mycursor=mydb.cursor()
mycursor.execute("SELECT * FROM Messages;")

myresult = mycursor.fetchall()

for i in myresult:
    print(i)




# import pymysql
# db = pymysql.connect(host='pluto.cse.msstate.edu',user='pjb183',passwd='csePluto!')
# cursor = db.cursor()
# query = ("SHOW DATABASES")
# cursor.execute(query)
# for r in cursor:
#     print(r)