document.addEventListener("DOMContentLoaded", function() {

    // Función para abrir el modal
    function openModal() {
        $('#payment-method-modal').modal('show');
    }

    // Función para cerrar el modal
    function closeModal() {
        $('#payment-method-modal').modal('hide');
    }

    // Obtener el token CSRF del formulario
    function getCSRFToken() {
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        return csrfToken;
    }

    // Abrir el modal al hacer clic en el botón "Agregar Tipo"
    document.getElementById("addPaymentMethod").addEventListener("click", openModal);

    // Manejar la creación de una nueva categoría
    document.getElementById("save-payment-method").addEventListener("click", function() {
        var formData = new FormData(document.getElementById("payment-method-form"));
        var csrfToken = getCSRFToken(); // Obtener el token CSRF
        if (csrfToken) {
            $.ajax({
                url: `/sales/payment-method/create`,
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
                            data.new_payment_method.name,
                            data.new_payment_method.id,
                            );
                        var idPaymentMethodSelect = document.getElementById("id_payment_method");
                        idPaymentMethodSelect.appendChild(newOption);
                        newOption.selected = true;
                        closeModal();  // Cerrar el modal después de agregar la nueva categoría
                    }else{
                        console.log(data.message);
                    }
                }
            });
        }
    });
});
