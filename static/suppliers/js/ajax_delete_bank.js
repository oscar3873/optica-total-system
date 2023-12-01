document.addEventListener("DOMContentLoaded", function() {

    var deleteButtons = document.querySelectorAll("#delete-button");
    let deleteModal = document.getElementById("delete-modal-body");

    var sendDelete = document.getElementById("delete-form-button");

    let id = 0;
    
    deleteButtons.forEach(function(button) {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            var info = this.getAttribute("data-info");
            deleteModal.textContent = `¿Desea eliminar la Cuenta: ${info} ?`;

            id = this.getAttribute("data-cbu-id");
        });
    });

    sendDelete.addEventListener("click", function() {
        let form_delete = document.getElementById("delete-form");
        var formData_bank = new FormData(form_delete);
        
        $.ajax({
            url: `/suppliers/ajax-delete-bank/${id}/`,  // Asegúrate de usar la URL correcta
            method: 'POST',
            data: formData_bank,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.status === 'success') {
                    $('#deleteModal').modal('hide');

                    let bank_deleted = document.getElementById(id);
                    id = 0;
                    bank_deleted.remove();
                    // Aquí puedes agregar lógica adicional después de eliminar
                } else {
                    console.log('Error al eliminar');
                }
            }
        });
    });
});
