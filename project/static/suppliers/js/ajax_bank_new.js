const bank_name_modal = document.getElementById("bank-name-form");
let error_bank = document.createElement('small');

const id_bank = document.getElementById('id_bank');

const id_bank_name = document.getElementById('id_bank_name');
id_bank_name.addEventListener('input', function() {
    error_bank.textContent = '';
});

document.addEventListener("DOMContentLoaded", function() {

    function regresarPrimerModal() {
        // Realizar la petición antes de volver al primer modal
        var formData_bank = new FormData(bank_name_modal);
        
        $.ajax({
            url: `/suppliers/ajax_bank_new`,  // Asegúrate de usar la URL correcta
            method: 'POST',
            data: formData_bank,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.status === 'success') {
                    data = data.bank_data;
                    console.log('Si paso');
                    var newOption = new Option(
                        data.name,
                        data.id,
                        );
                    id_bank.appendChild(newOption);
                    newOption.selected = true;
                    // Si la petición es exitosa, cerrar el segundo modal y mostrar el primero
                    $('#exampleModalToggle2').modal('hide');
                    $('#bankModal').modal('show');
                } else {
                    // Si hay un error, mostrar el mensaje de error en el mismo modal
                    let p_error = document.createElement('p');
                    p_error.className = 'm-0';
                    error_bank.innerHTML = data.error;
                    error_bank.className = "text-danger";

                    p_error.appendChild(error_bank)
                    
                    id_bank_name.parentNode.insertBefore(p_error, id_bank_name.nextSibling);
                }
            }
        });
    }

    // Manejar la creación de un nuevo banco y regresar al primer modal
    document.getElementById("save-bank-name").addEventListener("click", function() {
        regresarPrimerModal();
    });

});
