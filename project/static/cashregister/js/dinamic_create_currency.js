document.addEventListener("DOMContentLoaded", function() {

    // Función para abrir el modal
    function openModal() {
        $('#currency-modal').modal('show');
    }

    // Función para cerrar el modal
    function closeModal() {
        $('#currency-modal').modal('hide');
    }

    // Obtener el token CSRF del formulario
    function getCSRFToken() {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        return csrfToken;
    }

    // Abrir el modal al hacer clic en el botón "Agregar Tipo"
    document.getElementById("addCurrency").addEventListener("click", openModal);

    // Manejar la creación de una nueva categoría
    console.log(document.getElementById("save-currency"));
    document.getElementById("save-currency").addEventListener("click", function() {
        var formData = new FormData(document.getElementById("currency-form"));
        var csrfToken = getCSRFToken(); // Obtener el token CSRF
        console.log(formData);
        if (csrfToken) {
            $.ajax({
                url: `/cashregister/currency/create`,
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'X-CSRFToken': csrfToken // Incluir el token CSRF en los encabezados
                },
                success: function(data) {
                    if (data.status === 'success') {
                        var newOption = new Option(
                            data.new_currency.name, 
                            data.new_currency.id,
                            data.new_currency.symbol,
                            data.new_currency.code
                            );
                        var idCurrencySelect = document.getElementById("id_currency");
                        idCurrencySelect.appendChild(newOption);
                        newOption.selected = true;
                        closeModal();  // Cerrar el modal después de agregar la nueva categoría
                    }
                }
            });
        }
    });
});
