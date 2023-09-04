$(document).ready(function () {
    $('#agregarTipo').click(function () {
        // Abre una nueva ventana emergente con una URL vacía
        var nuevaVentana = window.open('', 'Nuevo Tipo de Caracteristica', 'width=600,height=400');

        // Cuando la ventana se abra, asigna la URL correcta
        nuevaVentana.location.href = $(this).data('url');

        // Espera a que se cierre la ventana emergente y luego realiza una petición AJAX para obtener el último Feature_type creado
        var comprobarCierre = setInterval(function () {
            if (nuevaVentana.closed !== false) {
                clearInterval(comprobarCierre);

                // Realiza una petición AJAX para obtener el último Feature_type creado y actualizar el campo type
                $.ajax({
                    type: 'GET',
                    url: '{% url "products_app:obtener_ultimo_feature_type" %}',
                    dataType: 'json',
                    success: function (data) {
                        if (data.type_id) {
                            console.log("Feature_type obtenido con éxito");
                            console.log(data);

                            // Actualiza el campo type con el Feature_type recién creado
                            $('#id_type').append($('<option>', {
                                value: data.type_id,
                                text: data.type_nombre
                            })).val(data.type_id);
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error("Error en la petición AJAX:", error);
                    }
                });
            }
        }, 1000);
    });
});
