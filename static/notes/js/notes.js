const noteSocket = new WebSocket('wss://' + window.location.host + '/ws/notes/global/'
);

noteSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message_note = data.message;

    // Contenedor principal de la nota
    const notesContainer = document.getElementById('notes-container');
    notesContainer.classList.add('notes-container');

    // Elemento de la nota
    const noteElement = document.createElement('div');
    noteElement.classList.add('notes', 'p-2', 'pb-1');

    // Etiqueta de la nota
    const noteLabel = document.createElement('div');
    noteLabel.style.backgroundColor = message_note.color;
    noteLabel.style.borderRadius = '6px';
    noteLabel.classList.add('note-label', 'px-2', 'py-1');

    const noteLabelText = document.createElement('p');
    noteLabelText.innerHTML = `<strong>${message_note.label}</strong>`;

    noteLabel.appendChild(noteLabelText);

    // Botón para cerrar la nota
    const closeNoteButton = document.createElement('button');
    closeNoteButton.textContent = '×';
    closeNoteButton.style.background = 'transparent';
    closeNoteButton.classList.add('close-note-button');

    // Agregar evento de clic al botón de cerrar
    closeNoteButton.addEventListener('click', function() {
        notesContainer.removeChild(noteElement);
    });

    // Contenido de la nota
    const noteContent = document.createElement('div');
    noteContent.classList.add('note-message');
    
    const notemessage = document.createElement('p');
    notemessage.innerHTML =  `<strong>${message_note.subject}:</strong> ${message_note.description}`;

    noteContent.appendChild(notemessage);

    const noteHeader = document.createElement('div');
    noteHeader.classList.add('d-flex', 'justify-content-between');

    noteHeader.appendChild(noteLabel);
    noteHeader.appendChild(closeNoteButton);

    // Agregar elementos a la nota
    noteElement.appendChild(noteHeader);
    noteElement.appendChild(noteContent);

    // Agregar la nota al contenedor
    notesContainer.appendChild(noteElement);

    var audioElement = document.createElement("audio");
    audioElement.id = "notes-audio";
    audioElement.autoplay = true; // Habilita el autoplay
    audioElement.muted = true; // Añade esta línea

    // Crea una fuente de audio
    var sourceElement = document.getElementById("notes-source");

    // Agrega la fuente de audio al elemento de audio
    audioElement.appendChild(sourceElement);

    // Agrega el elemento de audio al contenedor
    notesContainer.appendChild(audioElement);
    audioElement.play();
    
    // Eliminar la notificación después de 10 segundos (ajusta el tiempo según tus necesidades)
    // setTimeout(function() {
    //     notesContainer.removeChild(noteElement);
    // }, 10000); // 10000 milisegundos = 10 segundos
};
