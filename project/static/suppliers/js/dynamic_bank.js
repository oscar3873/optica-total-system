const bank_modal = document.getElementById("bank-form"); // Reemplaza con el ID del campo donde deseas mostrar el error
let error_div = document.createElement('div');

document.addEventListener("DOMContentLoaded", function() {

    function closeModal() {
        $('#bankModal').modal('hide');
    }
    // Manejar la creación de un nuevo banco
    document.getElementById("save-bank").addEventListener("click", function() {
        var formData = new FormData(bank_modal);
        
        $.ajax({
            url: `/suppliers/ajax-bank-supplier`,  // Asegúrate de usar la URL correcta
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.status === 'success') {
                    data = data.data;
                    var div_checksbox = document.createElement('div');
                    var newLabel = document.createElement('label');
                    var newCheckbox = document.createElement("input");
                    newCheckbox.type = "checkbox";
                    newCheckbox.name = "cbu"; // Asegúrate de asignar el nombre correcto
                    newCheckbox.hidden = true;
                    newCheckbox.value = data.id;
                    newCheckbox.className = "form-check-input";
                    newCheckbox.checked = true; // Define si está marcado o no
                    newLabel.htmlFor = newCheckbox.id;
                    newLabel.textContent = data.name; // Usa textContent para establecer el contenido del label
                    div_checksbox.classList = "form-check form-check-inline";
                    newLabel.appendChild(newCheckbox);
                    div_checksbox.appendChild(newLabel);
                    var checkboxes_form = document.getElementById('banks_asociate');
                    checkboxes_form.appendChild(div_checksbox);
                    closeModal();
                    var name_modal = document.getElementsByName('bank_name');
                    var cuit_modal = document.getElementsByName('cuit');
                    name_modal.textContent = '';  // Esto podría necesitar ajustes, dependiendo de cómo quieras borrar los campos del formulario
                    cuit_modal.textContent = '';  // Esto podría necesitar ajustes, dependiendo de cómo quieras borrar los campos del formulario

                } else {
                    error_div.innerHTML = data.error;
                    error_div.className = "text-danger text-center";
                    
                    bank_modal.appendChild(error_div);
                }
            }
        });
    });
});
