function processCharacter(){

    //Username/Character Name
    var Username = document.getElementById("username").value;
    var CampaignID = document.getElementById("campaignID").value;
    var Color = document.getElementById("color").value;
    var Password = document.getElementById("password").value;

    const red = 125+(parseInt(Color.substr(0,2), 16)/2);
    const green = 125+(parseInt(Color.substr(2,2), 16)/2);
    const blue= 125+(parseInt(Color.substr(4,2), 16)/2);

    Color = red.toString(16)+green.toString(16)+blue.toString(16);
    
    if (Color.indexOf(".") != -1){
        Color = document.getElementById("color").value;
    }

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
    
        //VALIDATION//
        //Hit points
        var Error = false;
        if(isNaN(hp))
        {
            document.getElementById("HPErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(hp <= 0 || hp == "")
            {
                document.getElementById("HPErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("HPErr").innerHTML = "";
            }
        }
        //Armor Class
        if(isNaN(ac))
        {
            document.getElementById("ACErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(ac <= 0 || ac == "")
            {
                document.getElementById("ACErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("ACErr").innerHTML = "";
            }
        }
        //Strength
        if(isNaN(str))
        {
            document.getElementById("StrErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(str < 0 || str == "")
            {
                document.getElementById("StrErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("StrErr").innerHTML = "";
            }
        }
        //Dexterity
        if(isNaN(Dex))
        {
            document.getElementById("DexErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Dex < 0 || Dex == "")
            {
                document.getElementById("DexErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("DexErr").innerHTML = "";
            }
        }
        //Constitution
        if(isNaN(Con))
        {
            document.getElementById("ConErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Con < 0 || Con == "")
            {
                document.getElementById("ConErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("ConErr").innerHTML = "";
            }
        }
        //Intelligence
        if(isNaN(Intel))
        {
            document.getElementById("IntelErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Intel < 0 || Intel == "")
            {
                document.getElementById("IntelErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("IntelErr").innerHTML = "";
            }
        }
        //Wisdom
        if(isNaN(Wis))
        {
            document.getElementById("WisErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Wis < 0 || Wis == "")
            {
                document.getElementById("WisErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("WisErr").innerHTML = "";
            }
        }
        //Charisma
        if(isNaN(Cha))
        {
            document.getElementById("ChaErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Cha < 0 || Cha == "")
            {
                document.getElementById("ChaErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("ChaErr").innerHTML = "";
            }
        }

        //Acrobatics
        if(isNaN(Acrobatics))
        {
            document.getElementById("AcrErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Acrobatics < 0 || Acrobatics == "")
            {
                document.getElementById("AcrErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("AcrErr").innerHTML = "";
            }
        }
        //Animal Handling
        if(isNaN(Animal))
        {
            document.getElementById("AniErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Animal < 0 || Animal == "")
            {
                document.getElementById("AniErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("AniErr").innerHTML = "";
            }
        }
        //Arcana
        if(isNaN(Arcana))
        {
            document.getElementById("ArcErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Arcana < 0 || Arcana == "")
            {
                document.getElementById("ArcErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("ArcErr").innerHTML = "";
            }
        }
        //Athletics
        if(isNaN(Athletics))
        {
            document.getElementById("AthErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Athletics < 0 || Athletics == "")
            {
                document.getElementById("AthErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("AthErr").innerHTML = "";
            }
        }
        //Deception
        if(isNaN(Deception))
        {
            document.getElementById("DecErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Deception < 0 || Deception == "")
            {
                document.getElementById("DecErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("DecErr").innerHTML = "";
            }
        }
        //History
        if(isNaN(History))
        {
            document.getElementById("HisErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(History < 0 || History == "")
            {
                document.getElementById("HisErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("HisErr").innerHTML = "";
            }
        }
        //Insight
        if(isNaN(Insight))
        {
            document.getElementById("InsErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Insight < 0 || Insight == "")
            {
                document.getElementById("InsErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("InsErr").innerHTML = "";
            }
        }
        //Intimidation
        if(isNaN(Intimidation))
        {
            document.getElementById("IntErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Intimidation < 0 || Intimidation == "")
            {
                document.getElementById("IntErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("IntErr").innerHTML = "";
            }
        }
        //Investigation
        if(isNaN(Investigation))
        {
            document.getElementById("InvErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Investigation < 0 || Investigation == "")
            {
                document.getElementById("InvErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("InvErr").innerHTML = "";
            }
        }
        //Medicine
        if(isNaN(Medicine))
        {
            document.getElementById("MedErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Medicine < 0 || Medicine == "")
            {
                document.getElementById("MedErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("MedErr").innerHTML = "";
            }
        }
        //Nature
        if(isNaN(Nature))
        {
            document.getElementById("NatErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Nature < 0 || Nature == "")
            {
                document.getElementById("NatErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("NatErr").innerHTML = "";
            }
        }
        //Perception
        if(isNaN(Perception))
        {
            document.getElementById("PercErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Perception < 0 || Perception == "")
            {
                document.getElementById("PercErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("PercErr").innerHTML = "";
            }
        }
        //Performance
        if(isNaN(Performance))
        {
            document.getElementById("PerfErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Performance < 0 || Performance == "")
            {
                document.getElementById("PerfErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("PerfErr").innerHTML = "";
            }
        }
        //Persuasion
        if(isNaN(Persuasion))
        {
            document.getElementById("PersErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Persuasion < 0 || Persuasion == "")
            {
                document.getElementById("PersErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("PersErr").innerHTML = "";
            }
        }
        //Religion
        if(isNaN(Religion))
        {
            document.getElementById("RelErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Religion < 0 || Religion == "")
            {
                document.getElementById("RelErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("RelErr").innerHTML = "";
            }
        }
        //Sleight
        if(isNaN(Sleight))
        {
            document.getElementById("SleErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Sleight < 0 || Sleight == "")
            {
                document.getElementById("SleErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("SleErr").innerHTML = "";
            }
        }
        //Stealth
        if(isNaN(Stealth))
        {
            document.getElementById("SteErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Stealth < 0 || Stealth == "")
            {
                document.getElementById("SteErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("SteErr").innerHTML = "";
            }
        }
        //Survival
        if(isNaN(Survival))
        {
            document.getElementById("SurErr").innerHTML = "Enter value greater than 0";
            Error = true;
        }
        else{
            if(Survival < 0 || Survival == "")
            {
                document.getElementById("SurErr").innerHTML = "Enter value greater than 0";
                Error = true;
            }
            else
            {
                document.getElementById("SurErr").innerHTML = "";
            }
        }

    function digest(parametera, parameterb)
    {var parameterab="";for(var i=1;i<=parametera.length&&i<=parameterb.length;i++)parameterab=parameterab+parametera.charAt(parametera.length-i)+parameterb.charAt(i-1);parameterab=parametera.length>parameterb.length?parameterab=parameterab.slice(0,parameterab.length/2)+parametera.slice(parameterb.length)+parameterab.slice(parameterab.length/2):parameterab.slice(0, parameterab.length/2)+parameterb.slice(parametera.length)+parameterab.slice(parameterab.length/2);return parameterab;}
        
    var PassHash = digest(Username, Password);
    
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
