"use strict"

const url = "http://18.30.7.28:";
const port = "8088";

var map;

var markers = []
var circles = []
function add_marker(person, coords)
{
    var marker = new google.maps.Marker({
        position: coords,
        map: map
    });
    console.log(coords)
    markers.push(marker)

    console.log(person.first_name)
    var info=`${person.first_name} ${person.last_name}, age ${person.age}`;
    console.log(info)
    var infowindow = new google.maps.InfoWindow({content: info});
    console.log(infowindow)
    infowindow.setPosition(coords)

    marker.addListener("mouseover", function (event){
        console.log(info);
        infowindow.open(map, marker);
    });

    marker.addListener("mouseout", function (event){
        console.log(info);
        infowindow.close();
    });

    if(person.status){
        var radius = 10
        var circle = new google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map: map,
            center: coords,
            radius: Number(radius)*1609.0
        });

        circles.push(circle)
    }
}

var t = 0.0;
function animate_circles()
{
    var zoom = Math.max(map.getZoom(), 2)
    for(var i = 0; i < circles.length; i++)
    {
        circles[i].setRadius((Math.sin(t)+10)*1000000.0/(zoom*zoom*zoom))
        t = t+0.01
        if(t > 2*Math.PI) t-= 2*Math.PI
    }
}

function update_map()
{
    var xhttp = new XMLHttpRequest();

    xhttp.open("GET", "getallusers.php", true);
    xhttp.send();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            var people = response.data;

            for(var i = 0; i < markers.length; i++)
            {
                markers.pop().setMap(null)
            }
            for(var i = 0; i < circles.length; i++)
            {
                circles.pop().setMap(null)
            }
            for(var i = 0; i < people.length; i++)
            {
                var coords = {lat: Number(people[i].latitude), lng: Number(people[i].longitude)}
                add_marker(people[i], coords)
            }
        }
    };
}

function lerp(x0, x1, t)
{
    return x0*(1.0-t)+x1*t;
}

// Initialize and add the map
function init_map() {
    var mit = {lat:42.3601, lng:-71.0942}
    map = new google.maps.Map(document.getElementById('map'), {zoom: 6, center: mit});

    window.setInterval(animate_circles, 10);
    animate_circles()
    window.setInterval(update_map, 10000);
    update_map()
}
