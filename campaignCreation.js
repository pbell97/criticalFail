function createCampaign ()
{
    var username = document.getElementById("username").value.trim();
    var password = document.getElementById("password").value.trim();
    var campaignID = document.getElementById("campaignID").value.trim();

    if (password.length < 8)
    {
        document.getElementById("passError").style.display = "block";
        return;
    }
    else
    {
        document.getElementById("passError").style.display = "none";
    }
    
    const encoder = new TextEncoder();
    var promise = window.crypto.subtle.digest("SHA-256", encoder.encode(username+password));
    promise.then(passhash =>
    {
        passhash = Array.from(new Uint8Array(passhash))
                        .map(byte => byte.toString(16).padStart(2,"0"))
                        .join("");

        $.ajax({
            url: "http://ec2-3-209-137-117.compute-1.amazonaws.com/createCampaign/",
            type: 'POST',
            data:{username: username, passhash: passhash, campaignID: campaignID},
            dataType: "JSON",
            async: true,
            success: function (data) {
                console.log("Login authenticated");
                document.cookie = "token="+data.token+"; expires="+data.expiration;
                window.location = "campaignPage.html";
                document.getElementById("error").style.display = "none";
            },
            failure: function (data) {
                console.log("Login failure");
                document.getElementById("error").style.display = "block";
            }
        });
    });
}

function goHome()
{
    window.location ="mainPage.html";
}