
let errorMessage = document.createElement("div");
const form_label = document.getElementById("id_label_form");
let errorField = form_label.querySelector('div[id="new_label"]');
let field = form_label.querySelector('input[id="id_label"]');

document.addEventListener("DOMContentLoaded", function() {
    function closeModal(){
        $('#note-label-modal').modal('hide');
        errorMessage.innerHTML = "";
        field.value = '';
    }

    document.getElementById("save-label").addEventListener("click",function(){
        let formData = new FormData(form_label);
        $.ajax({
            url: '/notes/new/label', // URL para enviar la solicitud POST
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if(data.status === 'success') {
                    // Crear una nueva opción para agregar al select
                    let newOption = new Option(data.new_type.label, data.new_type.id);
                    
                    // Obtener el elemento select por su ID
                    let idTypeSelect = document.getElementById("id_label");
                    let colorPickerDisabled = document.getElementById("color-input-disabled");
                    // Agregar la nueva opción al select
                    idTypeSelect.appendChild(newOption);
                    colorPickerDisabled.value = data.new_type.color;
                    // Seleccionar la nueva opción
                    newOption.selected = true;
                    
                    // Cerrar el modal después de agregar la etiqueta
                    closeModal();
                } else {
                    // Manejar errores de validación si la solicitud no fue exitosa
                    errorMessage.className = "text-danger";
                    errorMessage.textContent = "Este campo es requerido.";
                    
                    // Agregar el mensaje de error debajo del campo
                    errorField.appendChild(errorMessage);
                }
            }
        });

    })
})
