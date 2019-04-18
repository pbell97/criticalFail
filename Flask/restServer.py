from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from flask_cors import CORS, cross_origin
from flask_sslify import SSLify
import datetime
import mysql.connector
import secrets
import datetime
import random
import hashlib
import time

app = Flask(__name__)
sslify = SSLify(app)
# CORS(app, support_credentials=True)

print(" * Signing in to database...")
cnx = mysql.connector.connect(
    user='root',
    password='criticalFail',
    database='criticalFail',
    host='localhost',
    buffered=True)

sql = cnx.cursor(buffered=True)
# sql.execute('USE criticalfail;')
# sql.execute('SET GLOBAL connect_timeout=6000')



canSend = True
canSendTime = 0

def getSQLResults(query):
    global sql, canSend, canSendTime
    try:
        while(not canSend):
            if (canSendTime == 0):
                canSendTime = time.time()
            if (canSendTime != 0 and time.time() - canSendTime > 2):
                canSend = True
                canSendTime = 0
            print("sitting in loop")
            None
        canSend = False
        sql.execute(query)
        result = sql.fetchall()
        canSend = True
        canSendTime = 0
        if result == None:
            print("Repeating a search")
            result = getSQLResults(query)
        returnedItem = []
        for item in result:
            returnedItem.append(item)

        return returnedItem
    except Exception as exception:
        print("Got Error ", exception)
        return []

def postSQL(query, values):
    global sql, cnx
    sql.execute(query, values)
    cnx.commit()
    # try:
    #     result = sql.fetchall()
    # except:
    #     None

# getSQLResults("SET SQL_SAFE_UPDATES = 0;")


@app.route('/messages/', methods=['GET'], defaults={'lastMessageID': None, 'campaignID': None})
@app.route('/messages/<campaignID>/<lastMessageID>', methods=['GET'])
def getMessages(campaignID, lastMessageID):
    if (lastMessageID == None or campaignID == None):
        print("You didn't give a message ID or campaignID")
        return "You didn't give a message ID or campaignID or messageID didn't exist", 422

    messagesToSend = getSQLResults("SELECT * FROM cf_messages WHERE campaignID = '" + str(campaignID) + "' AND messageID >= " + str(lastMessageID))
    # print("Messages sending back are: ", messagesToSend)
    # messagesToSend = messages[int(lastMessageID):]

    # Use while loop for hanging request here?

    response = jsonify(messagesToSend)
    return response, 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/messages/', methods=['POST', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def postMessages():
    global messages

    # If there cookie doesn't match, give error and break
    if ('token' not in request.form.keys()):
        print("Un-authed user tried to post a message")
        return "Request is not correctly authorized", 403

    # Verifies token and gets user data
    token = request.form['token']
    tokenData = getSQLResults("SELECT username, campaignID FROM cf_tokens WHERE token = '" + token + "'")
    print("Token Data: ", tokenData)
    if (tokenData == []):
        print("Un-authed user tried to post a message")
        return "Request is not correctly authorized", 403

    if (hasTokenExpired(token)):
        print("Token expired.")
        return "Token has expired", 403

    username = tokenData[0][0]
    campaignID = tokenData[0][1]
    print("SELECT * FROM cf_users WHERE username = '" + username + "' AND campaignID = '" + str(campaignID) + "'")
    userData = getSQLResults("SELECT * FROM cf_users WHERE username = '" + username + "' AND campaignID = '" + str(campaignID) + "'")[0]
    color = userData[3]
    
    # print("UserData:", userData)

    # Get latest message id for this campaign
    latestID = getSQLResults("SELECT messageID FROM cf_messages WHERE campaignID = '" + str(campaignID) + "'")
    if (latestID != []):
        latestID = latestID[-1][0]
    else:
        latestID = 0
    newID = latestID + 1


    if ('contents' not in request.form.keys()):
        print("They done messed up")
        return "Didn't include contents param", 409
    elif (len(request.form['contents']) > 250):
        print("They done tried to put too long of a message")
        return "Message must be equal to or less than 250", 409
    elif (request.form['contents'].strip(" ") == ""):
        print("They done tried send to a blank message")
        return "Message must be equal to or less than 250", 409
    else:
        print("Got message",request.form['contents'])


        message = {"contents": request.form['contents'], "timestamp": datetime.datetime.now(), "id": newID, "user": username}
        postQuery = "INSERT INTO cf_messages (campaignID, messageID, message, username, time, recipient) VALUES (%s, %s, %s, %s, %s, %s)"
        postQueryValues = (str(campaignID), str(newID), request.form['contents'], username, str(message['timestamp']), 'none')
        postSQL(postQuery, postQueryValues)

        return jsonify(message), 201, {'Access-Control-Allow-Origin': '*'}

@app.route('/campaignsAll/', methods=['GET'])
# @cross_origin(supports_credentials=True)
def getAllCampaigns():
    campaigns = getSQLResults("SELECT * FROM cf_campaigns")
    returnObj = []
    for campaign in campaigns:
        if (campaign[0] == "Admin"):
            continue
        returnObj.append({"campaignID": campaign[0], "GMname": campaign[1]})

    for i in range(len(returnObj)):
        campaign = returnObj[i]["campaignID"]
        count = getSQLResults("SELECT COUNT(username) FROM cf_users WHERE campaignID = '" + str(campaign) + "'")
        returnObj[i]['count'] = count[0][0]
    return jsonify(returnObj), 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/playersAll/', methods=['GET'])
# @cross_origin(supports_credentials=True)
def getAllPlayers():
    players = getSQLResults("SELECT campaignID, username, color, attributes, GMflag FROM cf_users")
    returnObj = []
    for player in players:
        returnObj.append({"campaignID": player[0], "username": player[1], "color": player[2], "attributes": player[3], "GMflag": player[4]})
    return jsonify(returnObj), 200

@app.route('/adminDelete/', methods=['POST', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def adminDelete():
    # If there cookie doesn't match, give error and break
    if ('token' not in request.form.keys()):
        print("Un-authed user use admin page")
        return "Request is not correctly authorized", 403

    # Verifies token and gets user data
    token = request.form['token']
    tokenData = getSQLResults("SELECT username, campaignID FROM cf_tokens WHERE token = '" + token + "'")
    print("Token Data: ", tokenData)
    if (tokenData == [] or tokenData[0][0] != "Admin" or tokenData[0][1] != "Admin"):
        print("Un-authed user tried to use admin page")
        return "Request is not correctly authorized", 403

    if (hasTokenExpired(token)):
        print("Token expired.")
        return "Token has expired", 403

    delType = request.form['type']

    if (delType == "campaign"): 
        getSQLResults("DELETE FROM cf_messages WHERE campaignID = '" + str(request.form['campaignID']) + "'")
        getSQLResults("DELETE FROM cf_tokens WHERE campaignID = '" + str(request.form['campaignID']) + "'")
        getSQLResults("DELETE FROM cf_users WHERE campaignID = '" + str(request.form['campaignID']) + "'")
        getSQLResults("DELETE FROM cf_campaigns WHERE campaignID = \"" + request.form['campaignID'] + "\"")
    elif (delType == "player"):
        query = "DELETE FROM cf_users WHERE campaignID = \"" + request.form['campaignID'] + "\" AND username = \"" + request.form['username'] + "\""
        print("Q: " + query)
        getSQLResults("DELETE FROM cf_users WHERE campaignID = \"" + request.form['campaignID'] + "\" AND username = \"" + request.form['username'] + "\"")
        getSQLResults("DELETE FROM cf_tokens WHERE username = \"" + str(request.form['username']) + "\"")

    return "Success", 201, {'Access-Control-Allow-Origin': '*'}

@app.route('/login/', methods=['POST', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def postLogin():

    # Verifies token and gets user data
    username = request.form['username']
    passhash = request.form['passhash']
    passhash = hashlib.md5(passhash.encode()).hexdigest()
    campaignID = request.form['campaignID']
    usernameQuery = getSQLResults("SELECT * FROM cf_users WHERE username = '" + username + "' AND campaignID = '" + str(campaignID) + "'")
    
    print("Username query:", usernameQuery)

    # If user doesn't exist
    if (usernameQuery == []):
        return "Login Error", 400, {'Access-Control-Allow-Origin': '*'}

    # If password doesn't match
    if (usernameQuery[0][2] != passhash):
        return "Login Error", 400, {'Access-Control-Allow-Origin': '*'}
    else:
        # Generates token, 15 is bytes (each byte is 2 chars)
        token = secrets.token_hex(15)
        expirationTime = datetime.datetime.now() + datetime.timedelta(days=1)
    

    deletesAnyTokens = getSQLResults("DELETE FROM cf_tokens WHERE username = \"" + username + "\"AND campaignID = '" + str(campaignID) + "'")
    postQuery = "INSERT INTO cf_tokens (token, username, expiration, campaignID) VALUES (%s, %s, %s, %s)"
    postValues = (str(token), str(username), str(expirationTime), str(campaignID))
    postSQL(postQuery, postValues)

    return jsonify({"token": token, "expiration": expirationTime}), 201, {'Access-Control-Allow-Origin': '*'}

@app.route('/players/', methods=['GET'], defaults={'campaignID': None})
@app.route('/players/<campaignID>/', methods=['GET'])
def getPlayers(campaignID):
    if (campaignID == None):
        print("You didn't give a campaignID")
        return "You didn't give a campaignID ", 422

    players = getSQLResults("SELECT username, color FROM cf_users WHERE campaignID = '" + str(campaignID) + "' AND GMflag = 0")
    response = []

    for item in players:
        response.append({"username": item[0], "color": item[1]})

    response = jsonify(response)
    return response, 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/players/', methods=['GET'], defaults={'campaignID': None, "username": None})
@app.route('/players/<campaignID>/<username>/', methods=['GET'])
def getPlayerAttributes(campaignID, username):
    if (campaignID == None or username == None):
        print("You didn't give a campaignID or username")
        return "You didn't give a campaignID or username", 422

    attributes = getSQLResults("SELECT attributes FROM cf_users WHERE campaignID = " + str(campaignID) + " AND username = \"" + str(username) + "\"")

    if (len(attributes) == 1):
        attributes = attributes[0]
    

    response = jsonify(attributes)
    return response, 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/createPlayer/', methods=['POST', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def createPlayer():

    # Verifies token and gets user data
    campaignID = request.form['campaignID']
    username = request.form['username']

    if (campaignID == "Admin" and username != "Admin"):
        return "Can't join admin campaign", 400

    # Checks if user already exits
    userExistsQuery = getSQLResults("SELECT username FROM cf_users WHERE campaignID = \"" + str(campaignID) + "\" AND username = \"" + str(username) + "\"")

    if (userExistsQuery != []):
        return "User already exists", 400
    
    passHash = request.form['passhash']
    passHash = hashlib.md5(passHash.encode()).hexdigest()
    color = request.form['color']
    attributes = request.form['attributes']
    GMflag = 0

    # Makes sure campaign exists
    getResults = getSQLResults("SELECT campaignID FROM cf_campaigns WHERE campaignID = \"" + str(campaignID) + "\"")
    if (getResults == []):
        return "Campaign doesn't exist", 400

    # Adds user to database
    postQuery = "INSERT INTO cf_users (campaignID, username, password, color, attributes, GMflag) VALUES (%s, %s, %s, %s, %s, %s)"
    postValues = (str(campaignID), str(username), str(passHash), str(color),str(attributes), str(GMflag))
    postSQL(postQuery, postValues)

    # Creates token for new user
    token = secrets.token_hex(15)
    expirationTime = datetime.datetime.now() + datetime.timedelta(days=1)
    postQuery = "INSERT INTO cf_tokens (token, username, expiration, campaignID) VALUES (%s, %s, %s, %s)"
    postValues = (str(token), str(username), str(expirationTime), str(campaignID))
    postSQL(postQuery, postValues)

    return jsonify({"token": token, "expiration": expirationTime}), 201, {'Access-Control-Allow-Origin': '*'}

@app.route('/createCampaign/', methods=['POST', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def createCampaign():

    # Verifies token and gets user data
    campaignID = request.form['campaignID']
    GMname = request.form['username']

    # Checks if user already exits
    campaignExistsQuery = getSQLResults("SELECT campaignID FROM cf_campaigns WHERE campaignID = \"" + str(campaignID) + "\"")

    if (campaignExistsQuery != []):
        return "CampaignID already exists", 400
    
    passHash = request.form['passhash']
    passHash = hashlib.md5(passHash.encode()).hexdigest()
    
    # Adds campaign to database
    postQuery = "INSERT INTO cf_campaigns (campaignID, GMname) VALUES (%s, %s)"
    postValues = (str(campaignID), str(GMname))
    postSQL(postQuery, postValues)


    # Adds user to database
    postQuery = "INSERT INTO cf_users (campaignID, username, password, GMflag) VALUES (%s, %s, %s, %s)"
    postValues = (str(campaignID), str(GMname), str(passHash), str(1))
    postSQL(postQuery, postValues)

    # Creates token for new user
    token = secrets.token_hex(15)
    expirationTime = datetime.datetime.now() + datetime.timedelta(days=1)
    postQuery = "INSERT INTO cf_tokens (token, username, expiration, campaignID) VALUES (%s, %s, %s, %s)"
    postValues = (str(token), str(GMname), str(expirationTime), str(campaignID))
    postSQL(postQuery, postValues)

    return jsonify({"token": token, "expiration": expirationTime}), 201, {'Access-Control-Allow-Origin': '*'}

@app.route('/dice/', methods=['POST', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def postDiceRoll():
    # If there cookie doesn't match, give error and break
    if ('token' not in request.form.keys()):
        print("Un-authed user tried to roll dice")
        return "Request is not correctly authorized", 403

    # Verifies token and gets user data
    token = request.form['token']
    tokenData = getSQLResults("SELECT username, campaignID FROM cf_tokens WHERE token = '" + token + "'")
    print("Token Data: ", tokenData)
    if (tokenData == []):
        print("Un-authed user tried to roll dice")
        return "Request is not correctly authorized", 403

    if (hasTokenExpired(token)):
        print("Token expired.")
        return "Token has expired", 403


    username = tokenData[0][0]
    campaignID = tokenData[0][1]


    diceResults = []
    for i in range(int(request.form['numOfDice'])):
        dice = random.randint(1, int(request.form['sideNumber']))
        dice += int(request.form['modifier'])
        diceResults.append(dice)

    # Construct message with dice results
    message = username + " rolled "
    for roll in diceResults:
        message += str(roll) + ", "

    message = message[:-2] + "."

    # Get latest message id for this campaign
    latestID = getSQLResults("SELECT messageID FROM cf_messages WHERE campaignID = '" + str(campaignID) + "'")
    if (latestID != []):
        latestID = latestID[-1][0]
    else:
        latestID = 0
    newID = latestID + 1


    postQuery = "INSERT INTO cf_messages (campaignID, messageID, message, username, time, recipient) VALUES (%s, %s, %s, %s, %s, %s)"
    postQueryValues = (str(campaignID), str(newID), message, "Server", str(datetime.datetime.now()), 'none')
    postSQL(postQuery, postQueryValues)


    return "Success", 201, {'Access-Control-Allow-Origin': '*'}

# Checks if token has expired, if so, it deletes token
def hasTokenExpired(token):
    expiration = getSQLResults("SELECT expiration FROM cf_tokens WHERE token = \"" + str(token) + "\"")[0][0]
    print(expiration)
    expiration = datetime.datetime.strptime(expiration, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.datetime.now()

    hasExpired = now > expiration
    if (hasExpired):
        getSQLResults("DELETE FROM cf_tokens WHERE token = \"" + str(token) + "\"")
    
    return hasExpired


# NEEDS WORK!!!!
@app.route('/attributes/', methods=['POST', 'OPTIONS'])
def postPlayerAttributes():
    # If there cookie doesn't match, give error and break
    if ('token' not in request.form.keys()):
        print("Un-authed user tried to roll dice")
        return "Request is not correctly authorized", 403

    # Verifies token and gets user data
    token = request.form['token']
    tokenData = getSQLResults("SELECT username, campaignID FROM cf_tokens WHERE token = '" + token + "'")
    print("Token Data: ", tokenData)
    if (tokenData == []):
        print("Un-authed user tried to roll dice")
        return "Request is not correctly authorized", 403

    if (hasTokenExpired(token)):
        print("Token expired.")
        return "Token has expired", 403

    username = tokenData[0][0]
    campaignID = tokenData[0][1]

    attributes = str(request.form['attributes'])
    print("Atts: ", attributes)

    postQuery = "UPDATE cf_users SET attributes = '" + attributes + "' WHERE username = \"" + str(username) + "\" AND campaignID = \"" + str(campaignID) + "\";"
    # postValues =  (str(attributes))
    print(postQuery)
    # postSQL(postQuery, postValues)
    print(getSQLResults(postQuery))

    return "Success", 201, {'Access-Control-Allow-Origin': '*'}

@app.route('/GM/', methods=['GET'], defaults={'campaignID': None})
@app.route('/GM/<campaignID>/', methods=['GET'])
def getGM(campaignID):
    if (campaignID == None):
        print("You didn't give a campaignID or username")
        return "You didn't give a campaignID or username", 422

    GMusername = getSQLResults("SELECT username FROM cf_users WHERE campaignID = '" + str(campaignID) + "' AND GMFlag = 1")
    GMusername = GMusername[0][0]

    response = jsonify(GMusername)
    return response, 200, {'Access-Control-Allow-Origin': '*'}

@app.route('/currentPlayer/', methods=['GET'], defaults={'token': None})
@app.route('/currentPlayer/<token>/', methods=['GET'])
def getCurrentPlayer(token):
    if (token == None):
        print("You didn't give a token")
        return "You didn't give a token", 422

    tokenData = getSQLResults("SELECT username, campaignID FROM cf_tokens WHERE token = '" + token + "'")
    username = tokenData[0][0]
    stats = getSQLResults("SELECT * FROM cf_users WHERE username = '" + str(username) + "'")
    stats = stats[0]

    response = jsonify(stats)
    return response, 200, {'Access-Control-Allow-Origin': '*'}
   




app.run(host="0.0.0.0", port="80", debug=True, threaded=True)