
const checkboxes = document.querySelectorAll('.form-check-input');
const selectedProductsList = document.getElementById('selected-products-list');
let subtotal = 0.00;

function truncateString(str, maxLength) {
    return str.length > maxLength ? str.slice(0, maxLength - 3) + '...' : str;
}

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        const productRow = checkbox.closest('div.product-item');
        const productName = productRow.querySelector('.text-900');
        const productSalePriceText = productRow.querySelector('.text-600').innerText;
        const priceWithoutSymbol = productSalePriceText.replace('$', ''); // Elimina el símbolo "$"
        const productSalePrice = parseFloat(priceWithoutSymbol); // Convierte a flotante

        const quantityInput = productRow.querySelector(`#cantidad-${checkbox.id}`); // Utiliza el ID del input de cantidad
        const quantity = parseInt(quantityInput.value); // Obtén la cantidad

        if (checkbox.checked) {
            const truncatedProductName = truncateString(productName.innerText, 20);
            const listItem = document.createElement('tr');
            listItem.innerHTML = `
                <th class="fs-1 ps-0">${truncatedProductName}
                    <div class="fs--2 fs-md--1"><a class="text-danger" href="#!" onclick="removeProduct(this)">Quitar</a></div>
                </th>
                <th class="fs-1 pe-0 text-end">$ ${(productSalePrice * quantity).toFixed(2)}</th>
            `;

            listItem.dataset.productId = checkbox.id;
            selectedProductsList.appendChild(listItem);

            // Actualizar subtotal y total
            subtotal += productSalePrice * quantity;
            updateSubtotal(subtotal);

        } else {
            const listItemToRemove = selectedProductsList.querySelector(`tr[data-product-id="${checkbox.id}"]`);
            if (listItemToRemove) {
                selectedProductsList.removeChild(listItemToRemove);

                // Actualizar subtotal y total
                subtotal -= productSalePrice * quantity;
                updateSubtotal(subtotal);
            }
        }
    });
});

// Agregar evento clic a los botones de más y menos
const quantityButtons = document.querySelectorAll('.input-group[data-quantity] button');
quantityButtons.forEach(button => {
    button.addEventListener('click', () => {
        // PONER LOGICA PARA LOS BOTONES DE + Y -
    });
});

function calculateSubtotal() {
    const selectedProducts = selectedProductsList.querySelectorAll('tr');

    // Verificar si no hay productos seleccionados
    if (selectedProducts.length === 0) {
        return 0.0;
    }

    let subtotal = 0.0;
    quantityInputs.forEach(input => {
        const productRow = input.closest('div.product-item');
        const productSalePriceText = productRow.querySelector('.text-600').innerText;
        const priceWithoutSymbol = productSalePriceText.replace('$', ''); // Elimina el símbolo "$"
        const productSalePrice = parseFloat(priceWithoutSymbol); // Convierte a flotante
        const quantity = parseInt(input.value);

        subtotal += productSalePrice * quantity;
    });
    return subtotal;
}


function updateSubtotal(subtotal) {
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    if (subtotalElement && totalElement) {
        subtotalElement.innerText = `$ ${subtotal.toFixed(2)}`;
        totalElement.innerText = `$ ${subtotal.toFixed(2)}`;
    }
}

function removeProduct(link) {
    const listItem = link.closest('tr');
    if (!listItem) {
        return; // Salir de la función si el elemento no existe
    }
    const productId = listItem.dataset.productId;
    const checkbox = document.getElementById(productId);
    listItem.parentElement.removeChild(listItem);
    if (checkbox) {
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change')); // Dispara el evento 'change' para actualizar la lista
    }
}


// Actualizar subtotal al cargar la página
window.addEventListener('load', () => {
    const initialSubtotal = calculateSubtotal();
    updateSubtotal(initialSubtotal);
});
