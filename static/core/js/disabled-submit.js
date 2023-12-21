let buttons_submit = document.getElementsByClassName('guardar-formulario');

// Itera sobre la colección de elementos
Array.from(buttons_submit).forEach(button => {
    button.addEventListener("mouseup", () => {
 
        setTimeout(() => {
            button.type = "button";
        }, 1); // Ajusta el tiempo de espera según tus necesidades
    });
});
