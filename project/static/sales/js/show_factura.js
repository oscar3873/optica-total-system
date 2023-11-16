document.addEventListener('DOMContentLoaded', () => {
    // Obtener referencia al botón para ver la factura
    let buttonVerFactura = document.getElementById('factura');
    
    // Agregar evento click al botón
    buttonVerFactura.addEventListener('click', () => {
        // Obtener el ID de la venta desde el atributo data-id del botón
        const saleId = buttonVerFactura.getAttribute('data-id');
        
        // Realizar una solicitud AJAX para obtener la factura
        $.ajax({
            url: `/sales/show-factura/${saleId}/`, // Reemplaza con la ruta correcta
            method: 'GET',
            dataType: 'html',
            success: function(data) {
                // Crear una nueva pestaña o ventana y cargar el contenido HTML en ella
                var newTab = window.open();
                newTab.document.open();
                newTab.document.write(data);
                newTab.document.close();
            },
            error: function(xhr, status, error) {
                console.log("Error en la solicitud AJAX: " + error);
            }
        });
    });
});
