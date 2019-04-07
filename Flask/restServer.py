from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from flask_cors import CORS, cross_origin
from flask_sslify import SSLify
import datetime
import mysql.connector
import secrets
import datetime

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

@app.route('/serverInfo/', methods=['GET'])
# @cross_origin(supports_credentials=True)
def getServerInfo():
    global servers
    return jsonify(servers), 200

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





app.run(host="0.0.0.0", port="80", debug=True, threaded=True)