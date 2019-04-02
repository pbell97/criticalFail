#Make sure you add your password to the connector parameters
#Have MySQL insalled, Python 3.6, and python mysql connector
#MySQL connector only works with python 3.6 or below

#Questions
#is the token primary key in cf_users an int or string?
#what would be a reasonable length for usernames in all tables?
#Is color in cf_messages a string or HEX?
#Using bit to represent boolean in messages for the GMflag (0 = false, 1 = true)
#What is the message limit in cf_messages?


import mysql.connector

cnx = mysql.connector.connect(
    user='root',
    password='',
    host='localhost')

mycursor = cnx.cursor()

#Creates database criticalFail
mycursor.execute("CREATE DATABASE IF NOT EXISTS criticalFail")

#Creates table queries
"""
init_cf_tokens = "CREATE TABLE IF NOT EXISTS cf_tokens (token INT AUTO_INCREMENT NOT NULL, username VARCHAR(30), expiration DATE, PRIMARY KEY(token));"
init_cf_campaigns = "CREATE TABLE IF NOT EXISTS cf_campaigns (campaignID INT AUTO_INCREMENT NOT NULL, GMname VARCHAR(30), PRIMARY KEY(campaignID));"
init_cf_users = "CREATE TABLE IF NOT EXISTS cf_users (campaignID INT, username VARCHAR(30), password VARCHAR(128), color VARCHAR(30), attributes VARCHAR(256), GMflag INT, PRIMARY KEY(campaignID, username), FOREIGN KEY(campaignID) REFERENCES cf_campaigns(campaignID));"
init_cf_messages = "CREATE TABLE IF NOT EXISTS cf_messages (campaignID INT, messageID INT AUTO_INCREMENT NOT NULL, message __________, username VARCHAR(30), time TIME, recipient VARCHAR(30), PRIMARY KEY(campaignID, messageID) FOREIGN KEY(campaignID) REFERENCES cf_campaigns(campaignID));"
"""

#
"""
mycursor.execute(init_cf_tokens)
mycursor.execute(init_cf_campaigns)
mycursor.execute(init_cf_users)
mycursor.execute(init_cf_messages)
"""

"""
Series of test inserts

tokensTest = "INSERT INTO cf_tokens (username, expiration) VALUES ("Joe", 1999-04-01);"
campaignsTest = "INSERT INTO cf_campaigns (GMname) VALUES ("Phil");"
usersTest = "INSERT INTO cf_users (username, password, color, attributes, GMflag) VALUES ("Fred", "asdfavxdefasdf", "Blue", "testattribute", 0);"
messagesTest = "INSERT INTO cf_messages(message, username, time, recipient) VALUES ("Hello", "Joe", 19:00:00, "Fred");"

mycursor.execute(tokensTest)
mycursor.execute(campaignsTest)
mycursor.execute(usersTest)
mycursor.execute(messagesTest)


""" 

