// global_messages.js

const socket = new WebSocket(
    'ws://' + window.location.host + '/ws/global/'
);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data.message;
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    document.body.appendChild(messageElement);
};
