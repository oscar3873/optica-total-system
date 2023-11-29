document.addEventListener("DOMContentLoaded", function () {
    console.log("pasa por esta parte");
    const supplierBrands = document.getElementById('id_brands');
    const discountInput = document.getElementById('id_discount');

    // Función para habilitar o deshabilitar el campo de descuento
    function toggleDiscountField() {
        if (supplierBrands.value == "1") { // Cambia "1" al valor correcto del tipo de proveedor
            discountInput.setAttribute('disabled', 'true');
        } else {
            discountInput.removeAttribute("disabled");
        }
    }

    // Agregar evento al cambio del tipo de proveedor
    supplierBrands.addEventListener('change', toggleDiscountField);

    // Estilo para los checkboxes en caso de edición de proveedor
    const selectedBrandsContainer = document.getElementById('selected-brands-container');
    if (selectedBrandsContainer.classList.contains('update')) {
        const checkboxes = Array.from(selectedBrandsContainer.querySelectorAll('input[type="checkbox"]'));
        checkboxes.forEach(checkbox => {
            checkbox.classList.add('form-check-input');
        });
    }

    // Llamar a la función al cargar la página
    toggleDiscountField();
});
