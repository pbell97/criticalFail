$.ajax({
    url: "http://ec2-3-209-137-117.compute-1.amazonaws.com/campaignsAll/",
    type: 'GET',
    data: {},
    async: true,
    success: function (data) {
        var tableBody = "";
        for (campaign of data){
            tableBody += "<tr> <td>" + campaign.campaignID + "</td><td>" + campaign.count + "</td><td onclick='deleteCampaign(this)' style='cursor: pointer'>*DELETE*</td></tr>";
        }
        document.getElementsByTagName("table")[0].getElementsByTagName("tbody")[0].innerHTML = tableBody;
    },
    error: function(data) {
        console.log("Failed to get all campaign info");
    }
});


function deleteCampaign(element){
    var campaign = element.parentElement.getElementsByTagName('td')[0].innerText;
    $.ajax({
        url: "http://ec2-3-209-137-117.compute-1.amazonaws.com/adminDelete/",
        type: 'POST',
        data: {token: Cookies.get('token'), campaignID: campaign, type: "campaign"},
        async: true,
        success: function (data) {
            console.log("Deleted");
        },
        error: function(data) {
            console.log("Failed to get all campaign info");
        }
    });
}


// Logs out the admin
function logout(){
    Cookies.remove('token');//, { path: '' });
    Cookies.remove('campaignID');//, { path: '' });
    Cookies.remove('token', { path: '' });
    Cookies.remove('campaignID', { path: '' });
    window.location.href = "mainPage.html";
}