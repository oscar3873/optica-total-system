const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/global/'
);

function showNotification(message) {
    const notificationsContainer = document.createElement('div');
    notificationsContainer.classList.add('notifications-container');

    const notificationElement = document.createElement('div');
    notificationElement.classList.add('notification');
    notificationElement.textContent = message;

    notificationsContainer.appendChild(notificationElement);
    document.body.appendChild(notificationsContainer);

    setTimeout(function() {
        notificationsContainer.removeChild(notificationElement);
        if (notificationsContainer.children.length === 0) {
            document.body.removeChild(notificationsContainer);
        }
    }, 5000); // 5000 milisegundos = 5 segundos
}

notificationSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const notification = data.message;

    showNotification(notification);
};
