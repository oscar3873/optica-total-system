document.addEventListener("DOMContentLoaded", function() {

    const profileImageInput = document.querySelector('#id_imagen'); // Reemplaza con el ID real de tu campo de imagen
    const profileImagePreview = document.getElementById('profile-image-preview');
    const profileImageForm = document.getElementById('profile-image-form');
    const profileImageButtons = document.getElementById('profile-image-buttons');
    const cancelButtonImg = document.getElementById('cancel-img-button');

    const originalImage = profileImagePreview.src

    // Escuchar el evento "change" en el campo de imagen
    profileImageInput.addEventListener('change', function() {
        const selectedFile = profileImageInput.files[0];

        // Si se selecciona un archivo, mostrar la vista previa y los botones
        if (selectedFile) {
            const imageUrl = URL.createObjectURL(selectedFile);
            profileImagePreview.src = imageUrl;
            profileImageButtons.style.display = 'block';
        }
    });

    // Escuchar el evento "click" en el botón "Cancelar"
    cancelButtonImg.addEventListener('click', function() {
        // Restablecer el campo de entrada de imagen y ocultar la vista previa y los botones
        profileImageInput.value = ''; // Esto borra la selección de archivo
        profileImagePreview.src = originalImage; // Restablecer la vista previa a la imagen actual
        profileImageButtons.style.display = 'none';
    });

});
