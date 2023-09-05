jQuery(document).ready(function() {
    // Abrir una ventana emergente al hacer clic en el botón "agregarTipo"
    $('#agregarTipo').click(function() {
        var nuevaVentana = window.open('{% url "products_app:new_feature_type" %}', '_blank', 'height=400,width=600');
        // Establecer las dimensiones y características de la ventana emergente
        if (window.focus) {
            nuevaVentana.focus();
        }
    });

    // Manejar la creación de tipos de características y actualizar el selector 'type' (si es necesario)
    $('#crearTipoCaracteristica').click(function() {
        // Realizar una solicitud AJAX para crear el tipo de característica, si es necesario
        $.ajax({
            url: '{% url "products_app:new_feature_type" %}',
            method: 'POST',
            data: $('#formTipoCaracteristica').serialize(),
            success: function(data) {
                if (data.status === 'success') {
                    // Agregar el nuevo tipo de característica al campo 'type' (si lo deseas)
                    $('#id_type').append(data.new_option);
                    // Cierra la ventana emergente después de crear el tipo de característica
                    window.close();
                } else {
                    // Manejar errores si es necesario
                    console.log(data.errors);
                }
            }
        });
    });
});
