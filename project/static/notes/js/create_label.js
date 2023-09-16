document.getElementById("    ").addEventListener("click", function(){
    var formData = new FormData(document.getElementById("    "));

    $.ajax({
        url: ` /labels/new/label` ,
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            if(data.status == 'success') {
                var newOption = new Option(data.new_type.color, data.new_type.label, data.new_type.id);
                var idTypeSelect = document.getElementById("    ");
                idTypeSelect.appendChild(newOption);
                newOption.selected = true;
                closeModal();
            } else {
                var errorField = document.getElementById("id_label");
                var errorMessage = document.createElement("div")
                errorMessage.className = "text-danger";
                errorMessage.style.fontStyle = "italic";
                errorMessage.textContent = "Este campo es requerido.";
                // Resaltar el campo en rojo
                errorField.style.borderColor = "red";
            
                // Agregar el mensaje de error debajo del campo
                errorField.parentNode.appendChild(errorMessage);
            }
        }
    })
})