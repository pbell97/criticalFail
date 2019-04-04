function goToMainPage()
{
    var logo = document.getElementById("logoContainer");
    var subtitle = document.getElementById("subtitle");
    logo.style.height = "50%";
    subtitle.remove();

    var topRow = document.getElementById("topRowContainer");
    var bottomRow = document.getElementById("bottomRowContainer");
    topRow.style.opacity = "1";
    bottomRow.style.opacity = "1";
    
    var body = document.getElementsByTagName("body")[0];
    body.removeEventListener("click", goToMainPage);
    body.removeEventListener("keypress", goToMainPage);
};

function openLoginModal()
{
    var modal = document.getElementById("loginModal");
    modal.style.display = "block";    
};

function closeLoginModal()
{
    var modal = document.getElementById("loginModal");
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

// no idea what I'm doing
function login()
{
    var username = document.getElementById("username").value;
    $.ajax(
        {
            url: "mainPage.php",
            dataType: "text",
            // left PHP, right JS
            data: {username: username},
            method: "POST"
        }
    )
    .done(
        function (errorLogin)
        {
            var error = document.getElementById("errorMessage");
            error.innerHTML = errorLogin;
        }
    )
}