$.ajax({
    url: that.serverAddress + that.campaignID + "/" + that.latestMessageID,
    type: 'GET',
    data:{},
    async: true,
    success: function (data) {



    },
    error: function(data) {                 //TBH haven't used this, just looked this error part up for this specs page
        console.log("Get request failed");
    }

});

function jsonToTable(json){

    var ID = json.campaignID;
    var count = json.count;

    i = True;
    while(i){

        row += '<tr>' + '<td>' + ID + '<td>' + count + '<td>' + '*DELETE*' + '<td>'

        i = False;
    }




}

http://ec2-3-209-137-117.compute-1.amazonaws.com/campaignsAll/

http://ec2-3-209-137-117.compute-1.amazonaws.com/adminDelete/