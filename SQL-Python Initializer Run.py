#Make sure you add your password to the connector parameters
#Have MySQL insalled, Python 3.6, and python mysql connector
#MySQL connector only works with python 3.6 or below


import mysql.connector

cnx = mysql.connector.connect(
    user='root',
    password='',
    host='criticalfail',
    database = "criticalfail")

mycursor = cnx.cursor()

#Creates database criticalFail
mycursor.execute("CREATE DATABASE IF NOT EXISTS criticalfail;")

#Creates table queries
init_cf_tokens = "CREATE TABLE IF NOT EXISTS cf_tokens (token VARCHAR(32) NOT NULL, username VARCHAR(32), campaignID VARCHAR(32), expiration VARCHAR(32), PRIMARY KEY(token), FOREIGN KEY (campaignID) REFERENCES cf_campaigns(campaignID));"
init_cf_campaigns = "CREATE TABLE IF NOT EXISTS cf_campaigns (campaignID VARCHAR(32) NOT NULL, GMname VARCHAR(32), PRIMARY KEY(campaignID));"
init_cf_users = "CREATE TABLE IF NOT EXISTS cf_users (campaignID VARCHAR(32), username VARCHAR(32), password VARCHAR(128), color VARCHAR(32), attributes VARCHAR(1000), GMflag INT, PRIMARY KEY(campaignID, username), FOREIGN KEY(campaignID) REFERENCES cf_campaigns(campaignID));"
init_cf_messages = "CREATE TABLE IF NOT EXISTS cf_messages (campaignID VARCHAR(32), messageID INT NOT NULL, message VARCHAR(256), username VARCHAR(32), time VARCHAR(64), recipient VARCHAR(32), PRIMARY KEY(campaignID, messageID), FOREIGN KEY(campaignID) REFERENCES cf_campaigns(campaignID));"

mycursor.execute(init_cf_tokens)
mycursor.execute(init_cf_campaigns)
mycursor.execute(init_cf_users)
mycursor.execute(init_cf_messages)

#Series of test inserts

tokensTest = "INSERT INTO cf_tokens (token, username, campaignID, expiration) VALUES (%s, %s, %s, %s);"
tokensVal = ("ASDFGH", "Joe", "FFFFFFFFF" , "1999:04:01")

campaignsTest = "INSERT INTO cf_campaigns (campaignID, GMname) VALUES (%s, %s);"
campaignsVal = ("FFFFFFFFF", "Phil")

usersTest = "INSERT INTO cf_users (campaignID, username, password, color, attributes, GMflag) VALUES (%s, %s, %s, %s, %s, %s);"
usersVal = ("FFFFFFFFF", "Fred", "asdfavxdefasdf", "0xFFFFFF", "testattribute", 0)

messagesTest = "INSERT INTO cf_messages(campaignID, messageID, message, username, time, recipient) VALUES (%s, %s, %s, %s, %s, %s);"
messagesVal = ("FFFFFFFFF", 1, "Hello", "Joe", "19:00:00", "Fred")

mycursor.execute(tokensTest, tokensVal)
mycursor.execute(campaignsTest, campaignsVal)
mycursor.execute(usersTest, usersVal)
mycursor.execute(messagesTest, messagesVal)
    
"""myresult = mycursor.fetchall()

#==========================================================

for x in myresult:
    print(x)"""
