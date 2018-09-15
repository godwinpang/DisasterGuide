"use strict"

const myPort = 8085;

var connection = new WebSocket('ws://localhost:'+myPort);
var connectionOpen = false; 

connection.onopen = function() {
    console.log("client says: connection established!");
    connectionOpen = true; 

}

connection.onmessage = function(message) {
    console.log("message from server: " + message.data);
};

connection.onclose = function() {
    connectionOpen = false;
}


function conjureDisaster() {
    ///if(connectionOpen) {
        var specs = document.getElementById("disasterSpecs");
        var type = specs.disasterType.value;
        console.log(type);

        connection.send("this is an awesome message. - from Robot " + counter);


    //}
}

  