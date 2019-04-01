from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from flask_cors import CORS, cross_origin
from flask_sslify import SSLify
import datetime

app = Flask(__name__)
sslify = SSLify(app)
# CORS(app, support_credentials=True)


messages = []
servers = [{"campaignName": "First", "player": 5, "locked": True}, 
{"campaignName": "Two", "player": 10, "locked": True},
{"campaignName": "Three", "player": 2, "locked": False}]

tokens = {'abc123':"Patrick"}




@app.route('/messages/', methods=['GET'], defaults={'lastMessageID': None, 'campaignID': None})
@app.route('/messages/<campaignID>/<lastMessageID>', methods=['GET'])
def getMessages(campaignID, lastMessageID):
    global messages
    if (lastMessageID == None or campaignID == None or int(lastMessageID) > len(messages)):
        print("You didn't give a message ID or campaignID")
        return "You didn't give a message ID or campaignID or messageID didn't exist", 422

    messagesToSend = messages[int(lastMessageID):]

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

    if ( request.form['token'] not in tokens.keys()):
        print("Un-authed user tried to post a message")
        return "Request is not correctly authorized", 403

    if ('contents' not in request.form.keys()):
        print("They done messed up")
        return "Didn't include contents param", 409
    else:
        print("Got message",request.form['contents'])
        message = {"contents": request.form['contents'], "timestamp": datetime.datetime.now(), "id": len(messages), "user": tokens[request.form['token']]}

        messages.append(message)
        return jsonify(message), 201, {'Access-Control-Allow-Origin': '*'}

@app.route('/serverInfo/', methods=['GET'])
# @cross_origin(supports_credentials=True)
def getServerInfo():
    global servers
    return jsonify(servers), 200







app.run(host="0.0.0.0", port="80", debug=True, threaded=True)