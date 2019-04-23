function goToMainPage()
{
    const logo = document.getElementById("logoContainer");
    const subtitle = document.getElementById("subtitle");
    logo.style.height = "50%";
    subtitle.remove();

    document.getElementsByTagName("body")[0].style.backgroundColor = "";

    const topRow = document.getElementById("topRowContainer");
    const bottomRow = document.getElementById("bottomRowContainer");
    topRow.style.opacity = "1";
    bottomRow.style.opacity = "1";

    const links = document.getElementsByClassName("disabled");
    for (var i = links.length-1; i >= 0; i--)
    {
        links[i].classList.remove("disabled");
    }
    
    const body = document.getElementsByTagName("body")[0];
    body.removeEventListener("click", goToMainPage);
    body.removeEventListener("keypress", goToMainPage);
};

function openLoginModal()
{
    const modal = document.getElementById("loginModal");
    modal.style.display = "block";    
};

function closeLoginModal()
{
    const modal = document.getElementById("loginModal");
    modal.style.display = "none";  
}

function openFAQ()
{
    document.getElementById("FAQinfo").style.display = "block";    
};

function closeFAQ()
{
    document.getElementById("FAQinfo").style.display = "none";  
}

function login(){
    var serverAddress = "http://ec2-3-209-137-117.compute-1.amazonaws.com/login/";
    var campaignID = document.getElementById("campaignID").value.trim();
    var username = document.getElementById("username").value.trim();
    var password = document.getElementById("password").value.trim();

    var passhash = digest(username, password);

    $.ajax({
        url: serverAddress,
        type: 'POST',
        data:{username: username, passhash: passhash, campaignID: campaignID},
        async: true,
        success: function (data) {
            var error = document.getElementById("errorMessage");
            error.innerHTML = ""
            console.log("Post request passed")
            // Need to set cookie here and redirect
            Cookies.set("token", data.token);

            if (username == "Admin" && campaignID == "Admin"){
                window.location.href = "adminPage.html";
            } else{
                Cookies.set("campaignID", document.getElementById("campaignID").value.trim());
                window.location.href = "campaignPage.html";
            }

            
        },
        error: function(data) {
            var error = document.getElementById("errorMessage");
            error.innerHTML = "Bad login. Try again."
            console.log("Post request failed")
        }
    });
}

function digest(parametera, parameterb)
{var parameterab="";for(var i=1;i<=parametera.length&&i<=parameterb.length;i++)parameterab=parameterab+parametera.charAt(parametera.length-i)+parameterb.charAt(i-1);parameterab=parametera.length>parameterb.length?parameterab=parameterab.slice(0,parameterab.length/2)+parametera.slice(parameterb.length)+parameterab.slice(parameterab.length/2):parameterab.slice(0, parameterab.length/2)+parameterb.slice(parametera.length)+parameterab.slice(parameterab.length/2);return parameterab;}
