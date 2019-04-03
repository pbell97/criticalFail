// Chat class
function chatClass(serverAddress, currentSession) {
    this.serverAddress = serverAddress,
    this.chatWindow = document.getElementById("messagesPane");
    this.currentSession = currentSession;
    this.latestMessageID = 0;

    this.campaignID = 1;    // TESTING ONLY. Make this dynamic.

    this.sendMessage = function(text){
        var that = this;
        $.ajax({
            url: this.serverAddress,
            type: 'POST',
            data:{contents: text, token:Cookies.get('token')},
            async: true,
            success: function (data) {
                console.log("Got response from message post");
                var newMessage = new receivedMessage(data.contents, new Date(data.timestamp), data.id, data.user);
                console.log(newMessage.outputJson());
                document.getElementById("messageInput").value = "";
                that.displayMessage(newMessage);
                that.latestMessageID = newMessage.id + 1;
            }
        });
    }

    this.displayMessage = function(message){
        // Creates message element and adds content
        var messageElement = document.createElement('div');
        messageElement.classList.add("message");
        var messsageText = document.createElement('span');
        messsageText.innerText = message.contents;
        var messageInfo = document.createElement('p');
        messageInfo.innerText = message.user + " - " +  message.timestamp.toLocaleTimeString();

        // TODO: Set message color

        // Adds message to page
        messageElement.appendChild(messsageText);
        messageElement.appendChild(messageInfo);
        this.chatWindow.appendChild(messageElement);

        // Scrolls to bottom
        this.chatWindow.scrollTop = this.chatWindow.scrollHeight;
    }

    this.getMessages = function(){

        // Fixes several weird scopeing issues
            // 'that' is needed for scoping of successful ajax, and 'this.chat' needed for interval call
        if (typeof(this.serverAddress) == "undefined"){
            that = this.chat;
        } else {
            that = this;
        }

        $.ajax({
            url: that.serverAddress + this.campaignID + "/" + that.latestMessageID,
            type: 'GET',
            data:{},
            async: true,
            success: function (data) {

                // If there are messages, display and update latest message
                if (data.length != 0){
                    console.log("Got " + data.length +" new messages server");
                    for (var messageData of data){
                        var message = new receivedMessage(messageData[2], new Date(messageData[4]), messageData[1], messageData[3]);
                        that.displayMessage(message);
                    }
    
                    that.latestMessageID = message.id + 1;
                }
            }
        });

    }
    
}

// Recieved Message Class
function receivedMessage(contents, timestamp, id, user){
    this.contents = contents;
    this.timestamp = timestamp;
    this.id = id;
    this.user = user;

    this.outputJson = function(){
        return {contents: this.contents, timestamp: this.timestamp, id: this.id, user: this.user};
    }
}

// Get the input field
var messagesInputElement = document.getElementById("messageInput");

// Execute a function when the user releases a key on the keyboard
messagesInputElement.addEventListener("keyup", function(event) {
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    chat.sendMessage(this.value);
    
  }
});



var chat = new chatClass("http://ec2-3-209-137-117.compute-1.amazonaws.com/messages/", null);


// Need to set a timeout

// UNCOMMENT to do chatting if server is on, also need to set 'token' cookie to 'abc123'
// setInterval(chat.getMessages, 1000);