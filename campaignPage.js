// Chat class
function chatClass(serverAddress, currentSession) {
    this.serverAddress = serverAddress,
    this.chatWindow = document.getElementById("messagesPane");
    this.currentSession = currentSession;
    this.latestMessageID = 0;

    this.campaignID =  currentSession.campaignID;    // TESTING ONLY. Make this dynamic.

    this.sendMessage = function(text){
        if (this.currentSession.token == undefined){
            return;
        }

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

        var color = "FFFFFF";
        for (player of currentSession.players){
            if (player.username == message.user){
                color = player.color;
            }
        }

        messageInfo.innerHTML =  "<span style='color: #" + color + "'>" + message.user + "</span> - " +  message.timestamp.toLocaleTimeString();
        messsageText.style.color = "#"+color;

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
    this.GM = "";
    this.currentPlayer = "";
    this.currentPlayerData = {};

    // If its an observer, change some stuff
    if (this.token == undefined){
        document.getElementById("messageInput").style = "display: none";
        document.getElementById("logoutButton").innerHTML = "Go Home";
        document.getElementById("rollDice").style = "display: none";;
        document.getElementById("rightPanel").style = "display: none";
        document.getElementById("middlePanel").style = "right: 0rem";
        document.getElementById("messagesPane").style = "height: 100%";
    }


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


    this.populatePlayers = function(){
        for (player of this.players){
            var element = document.createElement("div");
            element.innerHTML = '<div class="playerName" style="background-color: #' + player.color + '">' + player.username +'</div>';
            document.getElementById("allPlayersView").appendChild(element);
        }
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
                that.populatePlayers();
            }
        });
        $.ajax({
            url: that.serverAddress + "GM/" + that.campaignID + "/",
            type: 'GET',
            data:{},
            async: true,
            success: function (data) {
                that.GM = data;
                document.getElementById("gmName").innerHTML = that.GM;
            }
        });
        if (this.token != undefined){
            $.ajax({
                url: that.serverAddress + "currentPlayer/" + Cookies.get('token') + "/",
                type: 'GET',
                data:{},
                async: true,
                success: function (data) {
                    that.currentPlayer = data[1];
                    that.currentPlayerData = JSON.parse(data[4])
                    document.getElementById("activePlayerView").getElementsByClassName("playerName")[0].innerHTML = that.currentPlayer;
                    that.populateStats()
                }
            });
        } else {
            document.getElementById("activePlayerView").getElementsByClassName("playerName")[0].innerHTML = "Observing";
        }
    }

    // Populates stats for current player
    this.populateStats = function(){
        document.getElementById("playerAttributeHP").value = this.currentPlayerData.medicine;
        document.getElementById("playerAttributeAC").value = this.currentPlayerData.athletics;
        document.getElementById("playerAttributeStr").value = this.currentPlayerData.str;
        document.getElementById("playerAttributeDex").value = this.currentPlayerData.dex;
        document.getElementById("playerAttributeCon").value = this.currentPlayerData.con;
        document.getElementById("playerAttributeInt").value = this.currentPlayerData.intel;
        document.getElementById("playerAttributeWis").value = this.currentPlayerData.wis;
        document.getElementById("playerAttributeCha").value = this.currentPlayerData.cha;
    }


    // http://ec2-3-209-137-117.compute-1.amazonaws.com/GM/campaignID/
    // Gets all players
    this.getCampaignPlayers();

    // Logs out the player
    this.logout = function(){
        Cookies.remove('token');//, { path: '' });
        Cookies.remove('campaignID');//, { path: '' });
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

function rollDice(step){
    if (step == "open"){
        content = `
        <div>Number of Dice: <input id="diceNumber"></div>
        <div>Number of sides on Dice: <input id="diceSideNumber"></div>
        <div><button onclick="rollDice('send')">Roll</button></div>
        `
        openModal(content);
        document.getElementById("mainModalContainer").onclick="";
    }
    if (step == "send"){
        $.ajax({
            url: "http://ec2-3-209-137-117.compute-1.amazonaws.com/dice/",
            type: 'POST',
            data:{token:Cookies.get('token'), sideNumber: document.getElementById("diceSideNumber").value, numOfDice: document.getElementById("diceNumber").value, modifier: 0},
            async: true,
            success: function (data) {
                console.log("Got response from message dice");

                document.getElementById("mainModalContainer").onclick="closeModal()";
                closeModal();
            }
        });
        
    }
}





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
setInterval(chat.getMessages, 1000);
