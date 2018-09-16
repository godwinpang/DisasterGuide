"use strict"

const port = 8085;

var connectionOpen = false;
var connection = new WebSocket("ws://localhost:"+port);

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

// function getDisasterSpecs()
// {
//     if(!connectionOpen) {
//         console.log("error: connection was closed")
//     }
//     return [specs, type, longitude, latitude, radius, severity]
// }

function conjureDisaster() {
    if(!connectionOpen) {
        console.log("error: connection was closed")
    }

    var specs = document.getElementById("disasterSpecs");
    var type = specs.disasterType.value;
    var longitude = specs.longitude.value;
    var latitude = specs.latitude.value;
    var radius = specs.radius.value;
    var severity = specs.severity.value;
    sendDisaster(specs, type, longitude, latitude, radius, severity)
}

function sendDisaster(specs, type, longitude, latitude, radius, severity) {
    var message=`{"type":${type},"longitude":${longitude},"latitude":${latitude},"radius":${radius},"severity":${severity}}`;
    console.log(message);

    connection.send(message);
}

function lerp(x0, x1, t)
{
    return x0*(1.0-t)+x1*t;
}

// Initialize and add the map
function init_map() {
    var mit = {lat:42.3601, lng:-71.0942}
    var map = new google.maps.Map(document.getElementById('map'), {zoom: 3, center: mit});

    map.addListener("click", function (event) {
        if(!connectionOpen) {
            console.log("error: connection was closed")
        }

        var specs = document.getElementById("disasterSpecs");
        var type = specs.disasterType.value;
        var radius = specs.radius.value;
        var severity = specs.severity.value;

        var specs = document.getElementById("disasterSpecs");
        var type = specs.disasterType.value;
        var longitude = specs.longitude.value;
        var latitude = specs.latitude.value;
        var radius = specs.radius.value;
        var severity = specs.severity.value;
        var message=`{"type":${type},"longitude":${longitude},"latitude":${latitude},"radius":${radius},"severity":${severity}}`;
        console.log(message);

        var low_r = 1.0;
        var low_g = 0.0;
        var low_b = 0.0;
        var high_r = 0.0;
        var high_g = 1.0;
        var high_b = 0.0;
        var t = Number(severity)/10.0;
        var r = 255*lerp(high_r, low_r, t);
        var g = 255*lerp(high_g, low_g, t);
        var b = 255*lerp(high_b, low_b, t);

        var color = `rgb(${r},${g},${b})`;
        console.log(color);
        var coords = event.latLng;
        var marker = new google.maps.Circle({
            strokeColor: color,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: color,
            fillOpacity: 0.35,
            map: map,
            center: coords,
            radius: Number(radius)*1609.0
        });
        specs.longitude.value = coords.lng();
        specs.latitude.value = coords.lat();
        marker.addListener("click", function (event){
            marker.setMap(null);

            //TODO: send message to server to delete
            // connection.send(message);
        });

        connection.send(message);
    });
}

function place_marker()
{
    var specs = document.getElementById("disasterSpecs");
    var type = specs.disasterType.value;
    var longitude = specs.longitude.value;
    var latitude = specs.latitude.value;
    var radius = specs.radius.value;
    var severity = specs.severity.value;

    var coords = {lat:longitude, lng:latitude}
}

//Vertex Shader Program
const vertex_shader_source = `
    attribute vec4 pos;

    uniform mat4 transform;

    void main() {
      gl_Position = transform*pos;
    }
  `;

//Fragment Shader Source
const fragment_shader_source = `
    void main() {
      gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
    }
  `;

//Load Shader of given a type and source
function load_shader(gl, type, source) {
    const shader = gl.createShader(type);

    gl.shaderSource(shader, source);
    gl.compileShader(shader);

    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
    }

    return shader;
}

//Compile a list of shaders into a program
function init_program(gl, types, sources)
{
    if(types.length != sources.length) alert('error: shader types and sources have different lengths');

    var shaders = [];
    const program = gl.createProgram();
    for(var s = 0; s < sources.length; s++)
    {
        shaders[s] = load_shader(gl, types[s], sources[s]);
        gl.attachShader(program, shaders[s]);
    }
    gl.linkProgram(program)

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(program));
        return null;
    }

    return program;
}

function init_buffers(gl) {
  // Create a buffer for the square's positions.
  const vertex_buffer = gl.createBuffer();

  // Select the positionBuffer as the one to apply buffer
  // operations to from here out.

  gl.bindBuffer(gl.ARRAY_BUFFER, vertex_buffer);

  // Now create an array of positions for the square.

  const positions = [
    -1.0,  1.0,
     1.0,  1.0,
    -1.0, -1.0,
     1.0, -1.0,
  ];

  // Now pass the list of positions into WebGL to build the
  // shape. We do this by creating a Float32Array from the
  // JavaScript array, then use it to fill the current buffer.

  gl.bufferData(gl.ARRAY_BUFFER,
                new Float32Array(positions),
                gl.STATIC_DRAW);

  return {position: vertex_buffer,};
}

function drawScene(gl, program_info, vertex_buffer) {
    gl.clearColor(0.0, 0.0, 0.0, 1.0);  // Clear to black, fully opaque
    gl.clearDepth(1.0);                 // Clear everything
    gl.enable(gl.DEPTH_TEST);           // Enable depth testing
    gl.depthFunc(gl.LEQUAL);            // Near things obscure far things

    transform = mat4.create()
    mat4.translate(transform,     // destination matrix
                   transform,     // matrix to translate
                   [0.0, 0.0, 0.0]);  // amount to translate

    {
        gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
        gl.vertexAttribPointer(
            program_info.attrib_locations.vertex_position,
            2, //number components
            gl.FLOAT, //type
            false, //normalize
            0, //bytes, 0 => calculate from number of components and type
            0 //offset in bytes
        );
        gl.enableVertexAttribArray(program_info.attrib_locations.vertex_position);
    }

    gl.useProgram(program_info.program);

    // Set the shader uniforms

    gl.uniformMatrix4fv(
        program_info.uniform_locations.transform,
        false,
        transform);
    gl.uniformMatrix4fv(
        programInfo.uniformLocations.modelViewMatrix,
        false,
        modelViewMatrix);

    {
        const offset = 0;
        const vertexCount = 4;
        gl.drawArrays(gl.TRIANGLE_STRIP, offset, vertexCount);
    }
}

function initGL()
{
    var canvas = document.getElementById('overlay_canvas');
    var gl = canvas.getContext('webgl');

    // Only continue if WebGL is available and working
    if (gl === null) {
        alert("Unable to initialize WebGL. Your browser or machine may not support it.");
        return;
    }

    const program = init_program(gl,
                                 [gl.VERTEX_SHADER, gl.FRAGMENT_SHADER],
                                 [vertex_shader_source, fragment_shader_source]);
    const program_info = {
        program: program,
        attrib_locations: {
            vertex_position: gl.getAttribLocation(program, 'pos'),
        },
        uniform_locations: {
            transform: gl.getUniformLocation(program, 'transform'),
        },
    };

    init_buffers(gl);

    //Clear the canvas
    gl.clearColor(1.0, 0.0, 0.0, 0.5);
    gl.clear(gl.COLOR_BUFFER_BIT);

}


// initGL();
