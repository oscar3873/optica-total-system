document.addEventListener("DOMContentLoaded", function() {

    // Función para abrir el modal
    function openModal() {
        $('#Product-category-modal').modal('show');
    }

    // Función para cerrar el modal
    function closeModal() {
        $('#Product-category-modal').modal('hide');
    }

    // Obtener el token CSRF del formulario
    function getCSRFToken() {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        return csrfToken;
    }

    // Abrir el modal al hacer clic en el botón "Agregar Tipo"
    document.getElementById("addCategory").addEventListener("click", openModal);

    // Manejar la creación de una nueva categoría
    document.getElementById("save-category").addEventListener("click", function() {
        var formData = new FormData(document.getElementById("Product-Category-form"));

        var csrfToken = getCSRFToken(); // Obtener el token CSRF

        if (csrfToken) {
            $.ajax({
                url: `/products/new/category/`,
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': csrfToken // Incluir el token CSRF en los encabezados
                },
                success: function(data) {
                    if (data.status === 'success') {
                        var newOption = new Option(data.new_category.name, data.new_category.id);
                        var idCategorySelect = document.getElementById("id_category");
                        idCategorySelect.appendChild(newOption);
                        newOption.selected = true;
                        closeModal();  // Cerrar el modal después de agregar la nueva categoría
                    }
                }
            });
        }
    });
});
