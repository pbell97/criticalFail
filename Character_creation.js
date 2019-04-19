function processCharacter(){

    //Username/Character Name
    var Username = document.getElementById("username").value;
    var CampaignID = document.getElementById("campaignID").value;
    var Color = document.getElementById("color").value;
    var Password = document.getElementById("password").value;

    //Attributes
    var hp = document.getElementById("HP").value;
    var ac = document.getElementById("AC").value;

    var str = document.getElementById("Str").value;
    var Dex = document.getElementById("Dex").value;
    var Con = document.getElementById("Con").value;
    var Intel = document.getElementById("Intel").value;
    var Wis = document.getElementById("Wis").value;
    var Cha = document.getElementById("Cha").value;

    //Skills
    var Acrobatics = document.getElementById("Acrobatics").value;
    var Animal = document.getElementById("Animal").value;
    var Arcana = document.getElementById("Arcana").value;
    var Athletics = document.getElementById("Athletics").value;
    var Deception = document.getElementById("Deception").value;
    var History = document.getElementById("History").value;

    var Insight = document.getElementById("Insight").value;
    var Intimidation = document.getElementById("Intimidation").value;
    var Investigation = document.getElementById("Investigation").value;
    var Medicine = document.getElementById("Medicine").value;
    var Nature = document.getElementById("Nature").value;
    var Perception = document.getElementById("Perception").value;

    var Performance = document.getElementById("Performance").value;
    var Persuasion = document.getElementById("Persuasion").value;
    var Religion = document.getElementById("Religion").value;
    var Sleight = document.getElementById("Sleight").value;
    var Stealth = document.getElementById("Stealth").value;
    var Survival = document.getElementById("Survival").value;

    var CharacterBackground = document.getElementById("background").value;
    
    var attributes = {
        hp : hp,
        ac : ac,

        str : str,
        dex : Dex,
        con : Con,
        intel : Intel,
        wis : Wis,
        cha : Cha,

        acrobatics : Acrobatics,
        animal : Animal,
        arcana : Arcana,
        athletics : Athletics,
        deceoption : Deception,
        history : History,
        insight : Insight,
        intimidation : Intimidation,
        investigation : Investigation,
        medicine : Medicine,
        nature : Nature,
        perception : Perception,
        performance : Performance,
        persuasion : Persuasion,
        religion : Religion,
        sleight : Sleight,
        stealth : Stealth,
        suvival : Survival,
        Character_Background: CharacterBackground, 
        GMflag: 0
    }
    /*
    if (password.length < 8)
    {
        document.getElementById("password").style.display = "block";
        return;
    }
    else
    {
        document.getElementById("passError").style.display = "none";
    }
    */
    function digest(parametera, parameterb)
    {var parameterab="";for(var i=1;i<=parametera.length&&i<=parameterb.length;i++)parameterab=parameterab+parametera.charAt(parametera.length-i)+parameterb.charAt(i-1);parameterab=parametera.length>parameterb.length?parameterab=parameterab.slice(0,parameterab.length/2)+parametera.slice(parameterb.length)+parameterab.slice(parameterab.length/2):parameterab.slice(0, parameterab.length/2)+parameterb.slice(parametera.length)+parameterab.slice(parameterab.length/2);return parameterab;}
        
    var PassHash = digest(Username, Password);
    
    //IMPLEMENT VALIDATION 

    $.ajax({
        url: "http://ec2-3-209-137-117.compute-1.amazonaws.com/createPlayer/",
        type: 'POST',
        data:{campaignID: CampaignID, username: Username, passhash: PassHash, color: Color, attributes: JSON.stringify(attributes)},
        async: true,
        success: function (data) {
            console.log("Got response from message post");
            // {"expiration": "ExpirationDate", "token": "30BitLongToken"}
            Cookies.set("token", data.token);
            Cookies.set("campaignID", document.getElementById("campaignID").value.trim());
            window.location.href = "campaignPage.html";
            document.getElementById("error").style.display = "none";
        },
        error: function(data) {                 //TBH haven't used this, just looked this error part up for this specs page
            console.log("Post request failed");
            document.getElementById("error").style.display = "block";
        }
    });
}

function updateModifier (element)
{
    const modifier = document.getElementById(element.id+"Mod");
    const modValue = Math.floor((element.value-10)/2);
    modifier.innerHTML = (modValue>0 ? "+" : "") + modValue;
}