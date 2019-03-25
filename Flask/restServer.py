from flask import Flask, jsonify, request
from flask_restful import Api, reqparse
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)


messages = []

@app.route('/messages/', methods=['GET'], defaults={'lastMessageID': None, 'campaignID': None})
@app.route('/messages/<campaignID>/<lastMessageID>', methods=['GET'])
def getMessages(campaignID, lastMessageID):
    global messages
    if (lastMessageID == None or campaignID == None or int(lastMessageID) > len(messages)):
        print("You didn't give a message ID or campaignID")
        return "You didn't give a message ID or campaignID or messageID didn't exist", 422

    messagesToSend = messages[int(lastMessageID):]

    response = "Return messages from " + str(lastMessageID) + " to present for campagin " + str(campaignID) + "\nMessages: " + str(messagesToSend)
    return response, 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/messages/', methods=['POST'])
@cross_origin(supports_credentials=True)
def postMessages():
    global messages
    if ('messageContents' not in request.args.keys()):
        print("They done messed up")
        return "Didn't include messageContents param", 409
    else:
        print(request.args['messageContents'])
        messages.append(request.args['messageContents'])
        return "Message Added", 201







app.run(debug=True, threaded=True)