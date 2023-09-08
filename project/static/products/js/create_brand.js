
// PETICION AJAX PARA MARCAS
document.getElementById("    ").addEventListener("click", function() {
    var formData = new FormData(document.getElementById("    "));

    $.ajax({
        url: `/products/new/brand/`,
        method: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            if (data.status === 'success') {
                var newOption = new Option(data.new_type.name, data.new_type.id);
                var idTypeSelect = document.getElementById("    ");
                idTypeSelect.appendChild(newOption);
                newOption.selected = true;
                closeModal();  // Cerrar el modal después de agregar el nuevo tipo
            } else {
                var errorField = document.getElementById("id_name"); // Reemplaza "id_name" con el ID de tu campo
                var errorMessage = document.createElement("div");
                errorMessage.className = "text-danger";
                errorMessage.style.fontStyle = "italic"; // Estilo en cursiva
                errorMessage.textContent = "Este campo es requerido.";
            
                // Resaltar el campo en rojo
                errorField.style.borderColor = "red";
            
                // Agregar el mensaje de error debajo del campo
                errorField.parentNode.appendChild(errorMessage);
            }
            
        }
    });
});