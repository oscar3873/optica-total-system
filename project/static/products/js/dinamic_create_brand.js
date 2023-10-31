document.addEventListener("DOMContentLoaded", function() {

    // Función para abrir el modal
    function openModal_brand() {
        $('#Product-brand-modal').modal('show');
    }

    // Función para cerrar el modal
    function closeModal_brand() {
        $('#Product-brand-modal').modal('hide');
    }

    // Obtener el token CSRF del formulario
    function getCSRFToken() {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        return csrfToken;
    }

    // Abrir el modal al hacer clic en el botón "Agregar Tipo"
    document.getElementById("addBrand").addEventListener("click", openModal_brand);

    // Manejar la creación de una nueva marca
    document.getElementById("save-brand").addEventListener("click", function() {
        var formData = new FormData(document.getElementById("Product-Brand-form"));

        var csrfToken = getCSRFToken(); // Obtener el token CSRF

        if (csrfToken) {
            $.ajax({
                url: `/products/new/brand/`,
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': csrfToken // Incluir el token CSRF en los encabezados
                },
                success: function(data) {
                    if (data.status === 'success') {
                        var newOption = new Option(data.new_brand.name, data.new_brand.id);
                        var idBrandSelect = document.getElementById("id_brand");
                        idBrandSelect.appendChild(newOption);
                        newOption.selected = true;
                        closeModal_brand();  // Cerrar el modal después de agregar la nueva marca
                    }else{
                        console.log(data.message);
                    }
                },
            });
        }
    });
});
