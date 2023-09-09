const notificationSocket = new WebSocket(`ws://${window.location.host}/ws/notifications/global/`);

document.addEventListener('DOMContentLoaded', () => {
    const notificationList = document.getElementById('notification-list');
    const notifIndicator = document.getElementById('navbarDropdownNotification');    

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

                // Verificar si hay nuevas notificaciones
                checkForNewNotifications(data.notifications);
            });
    }

    function showNotification(notification) {
        // Mostrar la notificación emergente
        const notificationsContainer = document.getElementById('notifications-app-container');

        const superdiv = appendNotification(notification);
        superdiv.classList.add('notifications-app');

        notificationsContainer.appendChild(superdiv);
        notificationsContainer.classList.add('notifications-app-container');

        const audioElement = document.createElement("audio");
        audioElement.autoplay = true; // Habilita el autoplay

        // Crea una fuente de audio
        const sourceElement = document.getElementById("notifications-source");

        // Agrega la fuente de audio al elemento de audio
        audioElement.appendChild(sourceElement);

        // Agrega el elemento de audio al contenedor
        notificationsContainer.appendChild(audioElement);


        setTimeout(() => {
            superdiv.style.animation = 'fadeOut 1s'; // Agrega la animación de desvanecimiento
            setTimeout(() => {
                notificationsContainer.removeChild(superdiv);
                notificationsContainer.removeChild(audioElement); // Elimina el elemento de audio
                notificationsContainer.appendChild(sourceElement);
            }, 1000); // Espera 1 segundo antes de eliminar la notificación y el elemento de audio
        }, 5000); // 5000 milisegundos = 5 segundos
    }

    function appendNotification(notification) {
        const notificationItem = document.createElement('div');
        notificationItem.classList.add('list-group-item');

        const notificationContent = document.createElement('div');
        notificationContent.classList.add('d-flex', 'align-items-center');

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('notification-avatar');

        const avatar = document.createElement('div');
        avatar.classList.add('avatar', 'avatar-2xl', 'mx-3');

        const img = document.createElement('img');
        img.classList.add('rounded-circle');
        img.src = notification.avatarSrc; // Reemplaza con la URL correcta de la imagen del avatar
        img.alt = '';

        avatar.appendChild(img);
        avatarDiv.appendChild(avatar);

        const notificationBody = document.createElement('div');
        notificationBody.classList.add('notification-body');

        const notificationText = document.createElement('p');
        notificationText.classList.add('mb-1');

        // Limita el texto del mensaje a 40 caracteres con "..."
        const truncatedText = String(notification.details).length > 40 ?
            `${notification.details.substring(0, 40)}...` :
            notification.details;

        notificationText.innerHTML = `<strong>${notification.user_made}</strong>: ${notification.reference_obj_verbose_name} ${truncatedText}`;

        const notificationTime = document.createElement('span');
        notificationTime.classList.add('notification-time');
        const date_formated = formatDateTime(notification.created_at);
        notificationTime.innerHTML = `<span class="me-2" role="img" aria-label="Emoji">💬</span>${date_formated}`;

        notificationBody.appendChild(notificationText);
        notificationBody.appendChild(notificationTime);

        notificationContent.appendChild(avatarDiv);
        notificationContent.appendChild(notificationBody);

        notificationItem.appendChild(notificationContent);

        const notif_href = document.createElement('a');
        notif_href.style.textDecoration = 'none';
        notif_href.href = '/home'; // DEBE MANDAR A LA URL QUE DEBERIA PASARSE POR EL JSON (AGREGAR AL JSON PASADO POR VIEW 'url' : notification.content_object.get_absolute_url())

        notif_href.appendChild(notificationItem);

        notificationList.appendChild(notif_href); // Agrega todo lo anterior a la lista de notificaciones

        return notificationItem;
    }

    function checkForNewNotifications(notifications) {
        // Variable para almacenar la fecha de la última notificación registrada en el almacenamiento de sesión
        let lastNotificationDate = localStorage.getItem('lastNotificationDate');
        let is_readNotifications = localStorage.getItem('is_readNotifications');

        if (notifications) {
            const latestNotificationDate = new Date(notifications[0].created_at).getTime();
            
            if (latestNotificationDate > lastNotificationDate) {
                // que la fecha registrada, mostrar el indicador
                notifIndicator.classList.add('notification-indicator', 'notification-indicator-danger');
                localStorage.setItem('is_readNotifications', 'false');

                // Actualiza la fecha de la última notificación en el almacenamiento de sesión
                localStorage .setItem('lastNotificationDate', latestNotificationDate.toString());
            }else {
                if(is_readNotifications == 'false'){
                    notifIndicator.classList.add('notification-indicator', 'notification-indicator-danger');
                }
                localStorage.setItem('lastNotificationDate', latestNotificationDate.toString());
            }
        }else {
            notifIndicator.classList.remove('notification-indicator', 'notification-indicator-danger');
        }
    }

    notificationSocket.addEventListener('message', (e) => {
        const data = JSON.parse(e.data);
        const notification = data.message;

        loadNotifications(notification);
        showNotification(notification);
    });

    if (notifIndicator) {
        notifIndicator.addEventListener('click', function () {
            notifIndicator.classList.remove('notification-indicator', 'notification-indicator-danger');
            localStorage.setItem('is_readNotifications', 'true');
        });
    }

    function formatDateTime(dateTimeString) {
        const formatDate = { year: 'numeric', month: '2-digit', day: '2-digit'};
        const formatTime = {hour: '2-digit', minute: '2-digit' };
        const dateTime = new Date(dateTimeString);
        const formattedDate = dateTime.toLocaleDateString('es-ES', formatDate);
        const formattedTime = dateTime.toLocaleTimeString('es-ES', formatTime);
        return `${formattedDate} - ${formattedTime}`;
    }
});
