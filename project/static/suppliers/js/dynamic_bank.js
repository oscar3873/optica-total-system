
console.log("Script ejecutado1");
document.addEventListener("DOMContentLoaded", function() {

    console.log("Script ejecutado1");
    function closeModal() {
        $('#bankModal').modal('hide');
    }
    console.log("Script ejecutado2");
    // Manejar la creación de un nuevo banco
    document.getElementById("save-bank").addEventListener("click", function() {
        var formData = new FormData(document.getElementById("bank-form"));
        console.log("Script ejecutado3");
        $.ajax({
            url: `/suppliers/ajax_bank_supplier`,  // Asegúrate de usar la URL correcta
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
                    console.log("Script ejecutado4");
                    newLabel.htmlFor = newCheckbox.id;
                    newLabel.textContent = data.name; // Usa textContent para establecer el contenido del label
                    div_checksbox.classList = "form-check form-check-inline";
                    newLabel.appendChild(newCheckbox);
                    div_checksbox.appendChild(newLabel);
                    console.log("Script ejecutado5");
                    var checkboxes_form = document.getElementById('checkboxes_form');
                    checkboxes_form.appendChild(div_checksbox);
                    console.log("Script ejecutado6");
                    closeModal();
                    var name_modal = document.getElementsByName('bank_name');
                    var cuit_modal = document.getElementsByName('cuit');
                    name_modal.textContent = '';  // Esto podría necesitar ajustes, dependiendo de cómo quieras borrar los campos del formulario
                    cuit_modal.textContent = '';  // Esto podría necesitar ajustes, dependiendo de cómo quieras borrar los campos del formulario

                } else {
                    var errorField = document.getElementById("ID DE DONDE VALLA EL ERROR A MOSTRAR"); // Reemplaza con el ID del campo donde deseas mostrar el error
                    var errorMessage = document.createElement("div");
                    errorMessage.className = "text-danger text-center";
                    errorMessage.style.fontSize = "0.8rem";
                    errorMessage.style.fontStyle = "italic";
                    errorMessage.textContent = "Hubo un error en la carga, por favor verifique los datos ingresados.";
                    console.log("Script ejecutado7");
                    // Resalta el campo en rojo
                    errorField.style.borderColor = "red";
                    console.log("Script ejecutado8");
                    // Agrega el mensaje de error debajo del campo
                    errorField.parentNode.appendChild(errorMessage);
                }
            }
        });
    });
});
