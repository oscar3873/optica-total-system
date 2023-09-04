const noteSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notes/global/'
);

noteSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message_note = data.message; // Cambiar "notification" por "message"
    
    const notificationElement = document.createElement('div');
    const notificationSound = document.createElement('audio');

    notificationElement.classList.add('notes');
    notificationElement.textContent = message_note;

    notificationSound.src = 'C:/Users/cofra/OneDrive/Escritorio/SaltaCode/Proyects/optica-total/project/static/notes/hgf/audio.mp3';
    notificationSound.autoplay = true;

    notificationElement.appendChild(notificationSound);
    console.log(notificationSound);

    const notesContainer = document.getElementById('notes-container'); // Usar "notes-container" en lugar de "notifications-container"
    notesContainer.appendChild(notificationElement);

    // Eliminar la notificación después de 10 segundos (ajusta el tiempo según tus necesidades)
    setTimeout(function() {
        notesContainer.removeChild(notificationElement);
    }, 10000); // 10000 milisegundos = 10 segundos
};
