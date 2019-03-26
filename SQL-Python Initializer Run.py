##Make sure you add your password to the connector parameters
##Have MySQL insalled, Python 3.6, and python mysql connector
##MySQL connector only works with python 3.6 or below

import mysql.connector

cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost')

mycursor = cnx.cursor()

##CODE THAT PURGES ALL DATABASES

##Creates database criticalFail
mycursor.execute("CREATE DATABASE testdb1")

##Creates tables
init_cf_users = "CREATE TABLE cf_users (ATTRIBUTES)"
init_cf_campaigns = ""
init_cf_messages = ""
init_cf_tokens = ""

##mycursor.execute(init_cf_users, init_cf_campaigns, init_cf_messages, init_cf_tokens)
##mycursor.execute(init_cf_users)
##mycursor.execute(init_cf_users)
##mycursor.execute(init_cf_users)
##mycursor.execute(init_cf_users)

##myresult = mycursor.fetchall()

#==========================================================

#for x in myresult:
#    print(x)
