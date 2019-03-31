// Chat class
function chatClass(serverAddress, currentSession) {
    this.serverAddress = serverAddress,
    this.chatWindow = document.getElementById("messagesPane");
    this.currentSession = currentSession;

    this.sendMessage = function(text){
        $.ajax({
            url: this.serverAddress,
            type: 'POST',
            data:{contents: text, token:Cookies.get('token')},
            async: true,
            success: function (data) {
                console.log("Got response from message post");
                var newMessage = new receivedMessage(data.contents, new Date(data.timestamp), data.id, data.user);
                console.log(newMessage.outputJson());
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




var chat = new chatClass("http://ec2-52-87-168-127.compute-1.amazonaws.com/messages/", null);