document.addEventListener('DOMContentLoaded', () => {

    let contenedorBotones = document.getElementById('gen-fatura-button');

    let buttonGenFactura = document.createElement('button');
    buttonGenFactura.textContent = 'Generar Factura';
    buttonGenFactura.classList.add("btn","btn-sm", "btn-primary", "m-2")
    buttonGenFactura.type = "submit";
    let option_selected = document.getElementById('id_select')
    let selectedValue = 0;
    buttonGenFactura.addEventListener("mouseup", () => {
        // Espera 500 milisegundos (0.5 segundos) antes de cambiar el tipo del botón
        setTimeout(() => {
            buttonGenFactura.type = "button";
        }, 1); // Ajusta el tiempo de espera según tus necesidades
    });
    // Agregar evento change al elemento <select>
    option_selected.addEventListener('change', () => {
        // Obtener el valor seleccionado
        selectedValue = option_selected.value;
        if(selectedValue != 0){
            contenedorBotones.appendChild(buttonGenFactura);
        }
        else{
            buttonGenFactura.remove()
        }
    });
});