/**
 * Esto esta para que cuando se termine de cargar el DOM capturamos todos los botones de delete
	* en la tabla de marca y los agregamos un evento click para que al hacer click se abra el modal
 * ademas capturamos a los botones de confirmacion y los asignamos a la url que se le paso por parametro
 * y tenemos una variable brandID que no esta siendo usada pero esta para futuras peticiones AJAX
 */

document.addEventListener("DOMContentLoaded", () => {
  
  const deleteButtons = document.querySelectorAll(
    '[data-bs-toggle="modal"][data-id]'
  );
  const confirmButton = document.querySelector(
    "#delete-brand-modal .btn-danger"
  );

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const brandId = this.getAttribute("data-id"); // para usar en un futuro
      const deleteUrl = this.getAttribute("data-url");
      confirmButton.href = deleteUrl;
    });
  });
});
