let button_submit = document.getElementById('guardar-formulario');
    button_submit.addEventListener("mouseup", () => {
        // Espera 500 milisegundos (0.5 segundos) antes de cambiar el tipo del botón
        setTimeout(() => {
            button_submit.type = "button";
        }, 1); // Ajusta el tiempo de espera según tus necesidades
    });