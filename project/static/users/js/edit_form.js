document.addEventListener("DOMContentLoaded", function() {
    const update_button_form = document.getElementById('Update_button_form');
    const cancel_button_form = document.getElementById('Cancel_button_form');
    
    update_button_form.addEventListener("click", enableEdit);
    cancel_button_form.addEventListener("click", cancelEdit);
    
    var name = document.getElementById('id_first_name').value;
    var last_name = document.getElementById('id_last_name').value;
    var dni = document.getElementById('id_dni').value;
    var address = document.getElementById('id_address').value;
    var phone_code = document.getElementById('id_phone_code').value;
    var phone = document.getElementById('id_phone_number').value;
    var email = document.getElementById('id_email').value;

    cancelEdit();
    
    function enableEdit() {
        // Habilitar la edición de campos en el formulario con la clase "update-form"
        const form = document.querySelector('[id^="singup"]');
        if (form) {
          form.querySelectorAll('input, select, textarea').forEach((el) => {
            el.removeAttribute('readonly');
            el.removeAttribute('disabled');
          });
    
          // Ocultar el botón "Editar" y mostrar los botones "Guardar Cambios" y "Cancelar"
          form.querySelector('.btn-primary').style.display = 'none';
          form.querySelector('.btn-warning').style.display = 'inline-block';
          form.querySelector('.btn-secondary').style.display = 'inline-block';
    
          // Actualizar el campo oculto para indicar que se está editando
          form.querySelector('[name="is_editable"]').value = 'true';
        }
      }
    
      function cancelEdit() {
        // Deshabilitar la edición de campos en el formulario con la clase "update-form"
        const form = document.querySelector('[id^="singup"]');
        if (form) {
          form.querySelectorAll('input, select, textarea').forEach((el) => {
            el.setAttribute('readonly', 'readonly');
            el.setAttribute('disabled', 'disabled');
          });
    
          // Mostrar el botón "Editar" y ocultar los botones "Guardar Cambios" y "Cancelar"
          form.querySelector('.btn-primary').style.display = 'inline-block';
          form.querySelector('.btn-warning').style.display = 'none';
          form.querySelector('.btn-secondary').style.display = 'none';
    
          // Actualizar el campo oculto para indicar que no se está editando
          form.querySelector('[name="is_editable"]').value = 'false';
        }
        if (name){
            document.getElementById('id_first_name').value = name;
            document.getElementById('id_last_name').value = last_name;
            document.getElementById('id_dni').value = dni;
            document.getElementById('id_address').value = address;
            document.getElementById('id_phone_code').value = phone_code;
            document.getElementById('id_phone_number').value = phone;
            document.getElementById('id_email').value = email;
        }
      }
});