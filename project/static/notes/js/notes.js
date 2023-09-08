const noteSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notes/global/'
);

noteSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message_note = data.message; // Cambiar "notification" por "message"
    
    const notificationElement = document.createElement('div');
    notificationElement.classList.add('notes');
    notificationElement.textContent = message_note;

    var audioElement = document.createElement("audio");
    audioElement.id = "notes-audio";
    audioElement.autoplay = true; // Habilita el autoplay

    // Crea una fuente de audio
    var sourceElement = document.getElementById("notes-source");

    // Agrega la fuente de audio al elemento de audio
    audioElement.appendChild(sourceElement);

    // Agrega el elemento de audio al contenedor    
    const notesContainer = document.getElementById('notes-container'); // Usar "notes-container" en lugar de "notifications-container"
    notesContainer.appendChild(audioElement);
    notesContainer.appendChild(notificationElement);
    
    audioElement.play();
    // Eliminar la notificación después de 10 segundos (ajusta el tiempo según tus necesidades)
    setTimeout(function() {
        notesContainer.removeChild(notificationElement);
    }, 10000); // 10000 milisegundos = 10 segundos
};
