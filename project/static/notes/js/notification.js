const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/global/'
);

notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const notification = data.message; // Cambiar "notification" por "message"
    
    const notificationElement = document.createElement('div');
    notificationElement.classList.add('notification');
    notificationElement.textContent = notification;

    const notificationsContainer = document.getElementById('notifications-container');
    notificationsContainer.appendChild(notificationElement);

    // Eliminar la notificación después de 5 segundos (ajusta el tiempo según tus necesidades)
    setTimeout(function() {
        notificationsContainer.removeChild(notificationElement);
    }, 5000); // 5000 milisegundos = 5 segundos
};
