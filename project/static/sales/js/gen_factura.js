document.addEventListener('DOMContentLoaded', () => {
    // Obtener referencia al botón para ver la factura
    let contenedorBotones = document.getElementById('contenedor-botones');

    let buttonGenFactura = document.createElement('button');
    buttonGenFactura.textContent = 'Generar Factura';
    buttonGenFactura.classList.add("btn", "btn-primary", "mt-2")
    let option_selected = document.getElementById('select-factura')
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

    // Agregar evento click al botón
    buttonGenFactura.addEventListener('click', () => {
        // Obtener el ID de la venta desde el atributo data-id del botón
    
        // Realizar una solicitud AJAX para obtener la factura
        $.ajax({
            url: `/sales/gen-factura/${serviceId}/${selectedValue}`, // Reemplaza con la ruta correcta
            method: 'GET',
            dataType: 'json',  // Cambiado a 'json'
            success: function (data) {
                window.location.reload();
            },
            error: function (xhr, status, error) {
                console.log("Error en la solicitud AJAX: " + error);
                // Manejar el error aquí, por ejemplo, mostrar un mensaje de error
            }
        });
    });
});
