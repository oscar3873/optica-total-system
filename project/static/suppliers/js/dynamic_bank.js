document.addEventListener("DOMContentLoaded", function() {
    
    function closeModal() {
        $('#bankModal').modal('hide');
    }
    // Manejar la creación de un nuevo Tipo de Características
    document.getElementById("save-bank").addEventListener("click", function() {
        var formData = new FormData(document.getElementById("bank-form"));

        $.ajax({
            url: `/supppliers/ajax_bank_supplier`,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.status === 'success') {
                    var div_checksbox = document.createElement('div');
                    var newLabel = document.createElement('label');
                    var newCheckbox = document.createElement("input");
                    newCheckbox.type = "checkbox";
                    newCheckbox.name = "bank"; // Asegúrate de asignar el nombre correcto
                    newCheckbox.value = data.id;
                    newCheckbox.className = "form-check-input";
                    newCheckbox.checked = true; // Define si está marcado o no
                    
                    newLabel.htmlFor = newCheckbox.id;
                    newLabel.textContent = data.name; // Usa textContent para establecer el contenido del label
                    div_checksbox.classList = "form-check form-check-inline";
                    newLabel.appendChild(newCheckbox);
                    div_checksbox.appendChild(newLabel);

                    var checkboxes_form = document.getElementById('checkboxes_form');
                    checkboxes_form.appendChild(div_checksbox);

                    closeModal();
                    var name_modal = document.getElementsByName('name');
                    var cuit_modal = document.getElementsByName('cuit');
                    name_modal.textContent = '';
                    cuit_modal.textContent = '';

                } else {
                    
                }
                
            }
        });
    });
});