document.addEventListener("DOMContentLoaded", function() {
	var brandBrandModal = document.getElementById("Product-brand-modal");

	// Función para abrir el modal
	function openModal() {
			$('#Product-brand-modal').modal('show');
	}

	// Función para cerrar el modal
	function closeModal() {
			$('#Product-brand-modal').modal('hide');
	}

	// Abrir el modal al hacer clic en el botón "Agregar Tipo"
	document.getElementById("addBrand").addEventListener("click", openModal);

	// Manejar la creación de un nuevo Tipo de Características
	document.getElementById("save-ft").addEventListener("click", 
	function() {
			var formData = new FormData(document.getElementById("Product-Brand-form"));

			jQuery.ajax({
					url: `/products/new/brand/`,
					method: 'POST',
					data: formData,
					processData: false,
					contentBrand: false,
					success: function(data) {
							if (data.status === 'success') {
									var newOption = new Option(data.new_brand.name, data.new_brand.id);
									var idBrandSelect = document.getElementById("id_brand");
									idBrandSelect.appendChild(newOption);
									newOption.selected = true;
									closeModal();  // Cerrar el modal después de agregar el nuevo tipo
							} else {
									var errorField = document.getElementById("id_name"); // Reemplaza "id_name" con el ID de tu campo
									var errorMessage = document.createElement("div");
									errorMessage.className = "text-danger";
									errorMessage.style.fontSize = "0.8rem";
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
});
