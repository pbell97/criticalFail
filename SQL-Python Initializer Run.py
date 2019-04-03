#Make sure you add your password to the connector parameters
#Have MySQL insalled, Python 3.6, and python mysql connector
#MySQL connector only works with python 3.6 or below

#Questions
#is the token primary key in cf_users an int or string?
#what would be a reasonable length for usernames in all tables?
#Is color in cf_messages a string or HEX?
#Using bit to represent boolean in messages for the GMflag (0 = false, 1 = true)
#What is the message limit in cf_messages?

#Probably need to change message time to DATE. Does 'DATE' include the time too?

import mysql.connector

print("Signing in to database...")
cnx = mysql.connector.connect(
    user='root',
    password='criticalFail',
    database='criticalFail',
    host='localhost')

mycursor = cnx.cursor()

#Creates database criticalFail
print("Creating Database...")
mycursor.execute("CREATE DATABASE IF NOT EXISTS criticalFail;")
mycursor.execute("USE criticalfail;")


#Creates table queries
init_cf_tokens = "CREATE TABLE IF NOT EXISTS cf_tokens (token VARCHAR(10) NOT NULL, username VARCHAR(30), expiration DATE, PRIMARY KEY(token));"
init_cf_campaigns = "CREATE TABLE IF NOT EXISTS cf_campaigns (campaignID INT AUTO_INCREMENT NOT NULL, GMname VARCHAR(30), PRIMARY KEY(campaignID));"
init_cf_users = "CREATE TABLE IF NOT EXISTS cf_users (campaignID INT, username VARCHAR(30), password VARCHAR(128), color VARCHAR(30), attributes VARCHAR(256), GMflag INT, PRIMARY KEY(campaignID, username), FOREIGN KEY(campaignID) REFERENCES cf_campaigns(campaignID));"
init_cf_messages = "CREATE TABLE IF NOT EXISTS cf_messages (campaignID INT, messageID INT NOT NULL, message VARCHAR(250), username VARCHAR(30), time VARCHAR(60), recipient VARCHAR(30), PRIMARY KEY(campaignID, messageID), FOREIGN KEY(campaignID) REFERENCES cf_campaigns(campaignID));"



print("Creating Tables...")
mycursor.execute(init_cf_tokens)
mycursor.execute(init_cf_campaigns)
mycursor.execute(init_cf_users)
mycursor.execute(init_cf_messages)


#Series of test inserts
tokensTest = 'INSERT INTO cf_tokens (token, username, expiration) VALUES ("abcde12345", "Fred", "1999-04-01");'
campaignsTest = 'INSERT INTO cf_campaigns (campaignID, GMname) VALUES ("1", "Phil");'
usersTest = 'INSERT INTO cf_users (campaignID, username, password, color, attributes, GMflag) VALUES ("1", "Fred", "asdfavxdefasdf", "Blue", "testattribute", 0);'
messagesTest = 'INSERT INTO cf_messages(campaignID, messageID, message, username, time) VALUES ("1", "1", "Hello", "Fred", "19:00:00");'

print("Inserting test data...")
mycursor.execute(tokensTest)
mycursor.execute(campaignsTest)
mycursor.execute(usersTest)
mycursor.execute(messagesTest)





