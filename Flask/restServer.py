from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from flask_cors import CORS, cross_origin
from flask_sslify import SSLify
import datetime
import mysql.connector
import secrets
import datetime
import random

app = Flask(__name__)
sslify = SSLify(app)
# CORS(app, support_credentials=True)

print(" * Signing in to database...")
cnx = mysql.connector.connect(
    user='root',
    password='criticalFail',
    database='criticalFail',
    host='localhost')

sql = cnx.cursor()
# sql.execute('USE criticalfail;')


messages = []
servers = [{"campaignName": "First", "player": 5, "locked": True}, 
{"campaignName": "Two", "player": 10, "locked": True},
{"campaignName": "Three", "player": 2, "locked": False}]
tokens = {'abc123':"Patrick"}


def getSQLResults(query):
    global sql
    sql.execute(query)
    try:
        result = sql.fetchall()
        returnedItem = []
        for item in result:
            returnedItem.append(item)

        return returnedItem
    except:
        return None

def postSQL(query, values):
    global sql, cnx
    sql.execute(query, values)
    cnx.commit()

# getSQLResults("SET SQL_SAFE_UPDATES = 0;")


@app.route('/messages/', methods=['GET'], defaults={'lastMessageID': None, 'campaignID': None})
@app.route('/messages/<campaignID>/<lastMessageID>', methods=['GET'])
def getMessages(campaignID, lastMessageID):
    if (lastMessageID == None or campaignID == None):
        print("You didn't give a message ID or campaignID")
        return "You didn't give a message ID or campaignID or messageID didn't exist", 422

    messagesToSend = getSQLResults("SELECT * FROM cf_messages WHERE campaignID = " + str(campaignID) + " AND messageID >= " + str(lastMessageID))
    print("Messages sending back are: ", messagesToSend)
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
    tokenData = getSQLResults("SELECT username FROM cf_tokens WHERE token = '" + token + "'")
    print("Token Data: ", tokenData)
    if (tokenData == []):
        print("Un-authed user tried to post a message")
        return "Request is not correctly authorized", 403

    username = tokenData[0][0]
    userData = getSQLResults("SELECT * FROM cf_users WHERE username = '" + username + "'")[0]
    color = userData[3]
    campaignID = userData[0]
    print("UserData:", userData)

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
        returnObj.append({"campaignID": campaign[0], "GMname": campaign[1]})
    return jsonify(returnObj), 200

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
    tokenData = getSQLResults("SELECT username FROM cf_tokens WHERE token = '" + token + "'")
    print("Token Data: ", tokenData)
    if (tokenData == [] or tokenData[0][0] != "Admin"):
        print("Un-authed user tried to use admin page")
        return "Request is not correctly authorized", 403

    delType = request.form['type']

    if (delType == "campaign"): 
        getSQLResults("DELETE FROM cf_campaigns WHERE campaignID = \"" + request.form['campaignID'] + "\"")
    elif (delType == "player"):
        query = "DELETE FROM cf_users WHERE campaignID = \"" + request.form['campaignID'] + "\" AND username = \"" + request.form['username'] + "\""
        print("Q: " + query)
        getSQLResults("DELETE FROM cf_users WHERE campaignID = \"" + request.form['campaignID'] + "\" AND username = \"" + request.form['username'] + "\"")


    return "Success", 201, {'Access-Control-Allow-Origin': '*'}

# Need to delete tokens when deleting players!!!

@app.route('/login/', methods=['POST', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def postLogin():

    # Verifies token and gets user data
    username = request.form['username']
    passhash = request.form['passhash']
    usernameQuery = getSQLResults("SELECT * FROM cf_users WHERE username = '" + username + "'")
    
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
    

    deletesAnyTokens = getSQLResults("DELETE FROM cf_tokens WHERE username = \"" + username + "\"")
    postQuery = "INSERT INTO cf_tokens (token, username, expiration) VALUES (%s, %s, %s)"
    postValues = (str(token), str(username), str(expirationTime))
    postSQL(postQuery, postValues)

    return jsonify({"token": token, "expiration": expirationTime}), 201, {'Access-Control-Allow-Origin': '*'}

@app.route('/players/', methods=['GET'], defaults={'campaignID': None})
@app.route('/players/<campaignID>/', methods=['GET'])
def getPlayers(campaignID):
    if (campaignID == None):
        print("You didn't give a campaignID")
        return "You didn't give a campaignID ", 422

    players = getSQLResults("SELECT username, color FROM cf_users WHERE campaignID = " + str(campaignID) + " AND GMflag = 0")
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

    # Checks if user already exits
    userExistsQuery = getSQLResults("SELECT username FROM cf_users WHERE campaignID = \"" + str(campaignID) + "\" AND username = \"" + str(username) + "\"")

    if (userExistsQuery != []):
        return "User already exists", 400
    
    passHash = request.form['passhash']
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
    postQuery = "INSERT INTO cf_tokens (token, username, expiration) VALUES (%s, %s, %s)"
    postValues = (str(token), str(username), str(expirationTime))
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
    postQuery = "INSERT INTO cf_tokens (token, username, expiration) VALUES (%s, %s, %s)"
    postValues = (str(token), str(GMname), str(expirationTime))
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
    tokenData = getSQLResults("SELECT username FROM cf_tokens WHERE token = '" + token + "'")
    print("Token Data: ", tokenData)
    if (tokenData == []):
        print("Un-authed user tried to roll dice")
        return "Request is not correctly authorized", 403

    username = tokenData[0][0]
    userData = getSQLResults("SELECT * FROM cf_users WHERE username = '" + username + "'")[0]
    campaignID = userData[0]


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





app.run(host="0.0.0.0", port="80", debug=True, threaded=True)