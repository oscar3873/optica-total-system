document.addEventListener('DOMContentLoaded', () => {

    let contenedorBotones = document.getElementById('gen-fatura-button');

    let buttonGenFactura = document.createElement('button');
    buttonGenFactura.textContent = 'Generar Factura';
    buttonGenFactura.classList.add("btn", "btn-primary")
    buttonGenFactura.type = "submit";
    let option_selected = document.getElementById('id_select')
    let selectedValue = 0;
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
        console.log('Opción seleccionada:', selectedValue);
    });
});