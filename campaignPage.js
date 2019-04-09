// Chat class
function chatClass(serverAddress, currentSession) {
    this.serverAddress = serverAddress,
    this.chatWindow = document.getElementById("messagesPane");
    this.currentSession = currentSession;
    this.latestMessageID = 0;

    this.campaignID =  currentSession.campaignID;    // TESTING ONLY. Make this dynamic.

    this.sendMessage = function(text){
        var that = this;

        // Trims text
        text = text.trim(" ");

        // Limits the message length
        if (text.length > 250){
            openModal("Your message cannot exceed 250 characters. Yours was " + text.length + ".");
            return;
        }

        // Doesn't send blank
        if (text == ""){
            return;
        }

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
            url: that.serverAddress + that.campaignID + "/" + that.latestMessageID,
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

function session(){
    this.serverAddress = "http://ec2-3-209-137-117.compute-1.amazonaws.com/";
    this.token = Cookies.get('token');
    this.campaignID = Cookies.get('campaignID');
    this.players = [];
    this.type = "";

    // If theres no campaignID token, go back home
    if (this.campaignID == null){
        window.location.href = "mainPage.html"; // May want to change this action. Maybe make a modal
    }

    // If no token, player is observer, clear everything that they can't use
    if (this.token == null){
        this.type = 'observer';
        // document.getElementById("logoutButton").outerHTML = "";
        // document.getElementById("allPlayersView").style = "top: 0%";
    }else {
        this.type = 'player';
    }

    this.getCampaignPlayers = function(){
        //http://ec2-3-209-137-117.compute-1.amazonaws.com/players/campaignID
        that = this;
        $.ajax({
            url: that.serverAddress + "players/" + that.campaignID + "/",
            type: 'GET',
            data:{},
            async: true,
            success: function (data) {
                that.players = data;
            }
        });

    }

    // Gets all players
    this.getCampaignPlayers();

    // Logs out the player
    this.logout = function(){
        Cookies.remove('token', { path: '' });
        Cookies.remove('campaignID', { path: '' });
        window.location.href = "mainPage.html";
    }



    // Need to populate users on side bar. Is this for User class?


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



function openModal(content)
{
    var modal = document.getElementById("mainModalContainer");
    modal.style.display = "block";    
    document.getElementById("mainModalContent").innerHTML = content;
};

function closeModal()
{
    var modal = document.getElementById("mainModalContainer");
    modal.style.display = "none";  
}


var currentSession = new session();
var chat = new chatClass("http://ec2-3-209-137-117.compute-1.amazonaws.com/messages/", currentSession);


// Need to set a timeout

// UNCOMMENT to do chatting if server is on, also need to set 'token' cookie to 'abc123'
// setInterval(chat.getMessages, 1000);
