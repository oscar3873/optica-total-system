
let button_print = document.getElementById('printer');;
const serviceId = button_print.getAttribute('data-id');

document.addEventListener('DOMContentLoaded', () => {
    button_print.addEventListener('click', () =>{
        $.ajax({
            url: `/sales/print_invoice/${serviceId}/`, // Reemplaza con la URL correcta de tu servidor
            method: 'GET',
            dataType: 'html', // Indica que esperas HTML en la respuesta
            success: function(data) {
                // Crea una nueva pestaña o ventana y carga el contenido HTML en ella
                var newTab = window.open();
                newTab.document.open();
                newTab.document.write(data);
                newTab.document.close();
            },
            error: function(xhr, status, error) {
                console.log("Error en la solicitud AJAX: " + error);
            }
        });
    })
});