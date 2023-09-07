const notificationSocket = new WebSocket(
    `ws://${window.location.host}/ws/notifications/global/`
);

document.addEventListener('DOMContentLoaded', () => {
    const notificationList = document.getElementById('notification-list');

    loadNotifications(); // Cargar notificaciones al cargar la página

    function loadNotifications() {
        fetch('/notifications/load/') // Reemplaza con la URL correcta de tu vista AJAX
            .then((response) => response.json())
            .then((data) => {
                // Procesa los datos y agrega las notificaciones a la lista
                notificationList.innerHTML = '';

                data.notifications.forEach((notification) => {
                    appendNotification(notification);
                });
            })
            .catch(() => {
                alert('Error al cargar las notificaciones.');
            });
    }

    function appendNotification(notification) {
        const notificationItem = document.createElement('div');
        notificationItem.classList.add('list-group-item');
        notificationItem.textContent = notification.details;

        if (!notification.is_read) {
            notificationItem.classList.add('unread');
        }

        notificationList.appendChild(notificationItem);
    }

    function showNotification(message) {
        // Mostrar la notificación en la lista de notificaciones
        const newNotification = {
            id: Date.now(), // Podrías generar un ID único aquí
            details: message,
            is_read: false
        };

        appendNotification(newNotification);

        // Mostrar la notificación emergente
        const notificationsContainer = document.getElementById('notifications-app-container');

        const notificationElement = document.createElement('div');
        notificationElement.classList.add('notifications-app');
        notificationElement.textContent = message;

        notificationsContainer.appendChild(notificationElement);
        notificationsContainer.classList.add('notifications-app-container');

        const audioElement = document.createElement("audio");
        audioElement.id = "notifications-audio";
        audioElement.autoplay = true; // Habilita el autoplay

        // Crea una fuente de audio
        const sourceElement = document.getElementById("notifications-source");

        // Agrega la fuente de audio al elemento de audio
        audioElement.appendChild(sourceElement);

        // Agrega el elemento de audio al contenedor
        notificationsContainer.appendChild(audioElement);

        setTimeout(() => {
            notificationElement.style.animation = 'fadeOut 1s'; // Agrega la animación de desvanecimiento
            setTimeout(() => {
                notificationsContainer.removeChild(notificationElement);
                notificationsContainer.removeChild(audioElement); // Elimina el elemento de audio
                notificationsContainer.appendChild(sourceElement);
            }, 1000); // Espera 1 segundo antes de eliminar la notificación y el elemento de audio
        }, 5000); // 5000 milisegundos = 5 segundos
    }

    notificationSocket.addEventListener('message', (e) => {
        const data = JSON.parse(e.data);
        const notification = data.message;

        showNotification(notification);
    });
});
