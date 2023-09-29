document.addEventListener("DOMContentLoaded", function() {

    const editButton = document.getElementById('edit-button');
    const editForm = document.getElementById('edit-form');
    const cancelButton = document.getElementById('cancel-button');

    if (editButton){
        editButton.addEventListener('click', () => {
            editButton.style.display = 'none';
            editForm.style.display = 'block';
        });
    }
    if (cancelButton){
        cancelButton.addEventListener('click', () => {
            editButton.style.display = 'block';
            editForm.style.display = 'none';
        });
    }
});