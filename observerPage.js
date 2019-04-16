$.ajax({
    url: "http://ec2-3-209-137-117.compute-1.amazonaws.com/campaignsAll/",
    type: 'GET',
    data: {},
    async: true,
    success: function (data) {
        var tableBody = "";
        for (campaign of data){
            tableBody += "<tr> <td>" + campaign.campaignID + "</td><td>" + campaign.count + "</td><td onclick='joinCampaign(this)' style='cursor: pointer'>*JOIN*</td></tr>";
        }
        document.getElementsByTagName("table")[0].getElementsByTagName("tbody")[0].innerHTML = tableBody;
    },
    error: function(data) {
        console.log("Failed to get all campaign info");
    }
});


function joinCampaign(element){
    var campaign = element.parentElement.getElementsByTagName('td')[0].innerText;
    Cookies.set('campaignID', campaign);
    window.location.href = "campaignPage.html";
}
