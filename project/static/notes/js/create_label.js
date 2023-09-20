document.addEventListener("DOMContentLoaded", function() {
    function closeModal(){
        $('#note-label-modal').modal('hide');
    }

    document.getElementById("save-label").addEventListener("click",function(){
        var formData = new FormData(document.getElementById("id_label_form"));
        $.ajax({
            url: '/notes/new/label', // URL para enviar la solicitud POST
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if(data.status === 'success') {
                    console.log('Adding new option to select');
                    // Crear una nueva opción para agregar al select
                    var newOption = new Option(data.new_type.label, data.new_type.id);
                    
                    // Obtener el elemento select por su ID
                    var idTypeSelect = document.getElementById("id_label");
                    var colorPickerDisabled = document.getElementById("color-input-disabled");
                    // Agregar la nueva opción al select
                    idTypeSelect.appendChild(newOption);
                    colorPickerDisabled.value = data.new_type.color;
                    // Seleccionar la nueva opción
                    newOption.selected = true;
                    
                    // Cerrar el modal después de agregar la etiqueta
                    console.log('Closing modal');
                    closeModal();
                } else {
                    // Manejar errores de validación si la solicitud no fue exitosa
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
        });

    })
})
