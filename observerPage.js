request = new XMLHttpRequest()
request.onreadystatechange = function(){
    if(request.readyState === 4 && request.status === 200){
         console.log(this.responseText);
    }
}
request.open("GET", "http://ec2-3-208-34-201.compute-1.amazonaws.com:80/serverInfo/", true);
request.send();


