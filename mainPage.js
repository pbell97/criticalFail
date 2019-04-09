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

// not done - still need error checking, password hashing, etc.
function login(){
    var serverAddress = "http://ec2-3-209-137-117.compute-1.amazonaws.com/login/";
    var campaignID = document.getElementById("campaignID").value.trim();
    var username = document.getElementById("username").value.trim();
    var password = document.getElementById("password").value.trim();

    $.ajax({
        url: serverAddress,
        type: 'POST',
        data:{username: username, passhash: password, campaignID: campaignID},
        async: true,
        success: function (data) {
            var error = document.getElementById("errorMessage");
            error.innerHTML = ""
            console.log("Post request passed")
            // Need to set cookie here and redirect
        },
        error: function(data) {
            var error = document.getElementById("errorMessage");
            error.innerHTML = "invalid data"
            console.log("Post request failed")
        }
    });
}