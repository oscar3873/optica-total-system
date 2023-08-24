// static/websocket.js
var socket = new WebSocket("ws://yourdomain/ws/objects/");

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    if (data.message_type === 'object_created') {
        // Manipula la información del objeto creado
    }
};
