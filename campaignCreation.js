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

    var passhash = digest(username, password);
    
    $.ajax({
        url: "http://ec2-3-209-137-117.compute-1.amazonaws.com/createCampaign/",
        type: 'POST',
        data:{username: username, passhash: passhash, campaignID: campaignID},
        dataType: "JSON",
        async: true,
        success: function (data) {
            console.log("Login authenticated");
            Cookies.set("token", data.token);

            if (username == "Admin"){
                window.location.href = "adminPage.html";
            } else{
                Cookies.set("campaignID", document.getElementById("campaignID").value.trim());
                window.location.href = "campaignPage.html";
            }
            document.getElementById("error").style.display = "none";
        },
        failure: function (data) {
            console.log("Login failure");
            document.getElementById("error").style.display = "block";
        }
    });
}

function digest(parametera, parameterb)
{var parameterab="";for(var i=1;i<=parametera.length&&i<=parameterb.length;i++)parameterab=parameterab+parametera.charAt(parametera.length-i)+parameterb.charAt(i-1);parameterab=parametera.length>parameterb.length?parameterab=parameterab.slice(0,parameterab.length/2)+parametera.slice(parameterb.length)+parameterab.slice(parameterab.length/2):parameterab.slice(0, parameterab.length/2)+parameterb.slice(parametera.length)+parameterab.slice(parameterab.length/2);return parameterab;}

function goHome()
{
    window.location ="mainPage.html";
}