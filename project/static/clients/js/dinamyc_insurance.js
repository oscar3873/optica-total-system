document.addEventListener("DOMContentLoaded", function() {
    
    function closeModal() {
        $('#HI-modal').modal('hide');
    }
    // Manejar la creación de un nuevo Tipo de Características
    document.getElementById("save-hi").addEventListener("click", function() {
        var formData = new FormData(document.getElementById("HI-form"));

        var checkboxes = document.querySelectorAll('[id^="id_h_insurance_"]');
        var countchecks = checkboxes.length;

        $.ajax({
            url: `/customers/health_insurance/new/`,
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
                    newCheckbox.name = "h_insurance"; // Asegúrate de asignar el nombre correcto
                    newCheckbox.value = data.new_insurance.id;
                    newCheckbox.className = "form-check-input";
                    newCheckbox.id = "id_h_insurance_" + countchecks; // Un ID único para cada checkbox
                    newCheckbox.checked = true; // Define si está marcado o no
                    
                    newLabel.htmlFor = newCheckbox.id;
                    newLabel.textContent = data.new_insurance.name; // Usa textContent para establecer el contenido del label
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
                    var errorField = document.getElementById("form-to-new-checks"); // Reemplaza "id_name" con el ID de tu campo
                    var errorMessage = document.createElement("div");
                    errorMessage.className = "text-danger text-center";
                    errorMessage.style.fontSize = "0.8rem";
                    errorMessage.style.fontStyle = "italic"; // Estilo en cursiva
                    errorMessage.textContent = "Hubo un error en la carga, porfavor verifique los datos ingresados.";
                
                    // Resaltar el campo en rojo
                    errorField.style.borderColor = "red";
                
                    // Agregar el mensaje de error debajo del campo
                    errorField.parentNode.appendChild(errorMessage);
                }
                
            }
        });
    });
});