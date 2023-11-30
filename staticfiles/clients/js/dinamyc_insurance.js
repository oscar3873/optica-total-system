const hi_form = document.getElementById("HI-form");
var errorMessage = document.createElement("div");


document.addEventListener("DOMContentLoaded", function() {
    
    function closeModal() {
        $('#HI-modal').modal('hide');
        document.getElementById('id_name').value = '';
        document.getElementById('id_cuit').value = '';
        let phone = hi_form.querySelector('input[name="phone_number"]');
        phone.value = '';
        errorMessage.innerHTML = '';
    }
    // Manejar la creación de un nuevo Tipo de Características
    document.getElementById("save-hi").addEventListener("click", function() {
        var formData = new FormData(hi_form);

        var checkboxes = document.querySelectorAll('[id^="id_h_insurance_"]');
        var countchecks = checkboxes.length;

        $.ajax({
            url: `/customers/health-insurance/new/`,
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

                } else if (data.error){
                    errorMessage.className = "text-danger text-center my-2";
                    errorMessage.innerHTML = data.error;
                
                    hi_form.appendChild(errorMessage);
                }
                
            }
        });
    });
});