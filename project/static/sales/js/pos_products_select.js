document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-product');
    const findsProductsContainer = document.getElementById('product-container');
    const selectproductsContainer = document.getElementById('selected-products-list'); 
    const subtotalElement = document.getElementById('subtotal');

    const totalElement = document.getElementById('total');
    const discountElement = document.getElementById('discount');
    const TotalSuccess = document.getElementById('total-success');

    // Guardar productos seleccionados
    const selectedProducts = [];

    findsProductsContainer.innerHTML = 'Aqui veras los productos de la busqueda.';

    function truncateString(str, maxLength) {
        return str.length > maxLength ? str.slice(0, maxLength - 3) + '...' : str;
    }

    // Event listener para el campo de búsqueda
    searchInput.addEventListener('input', handleSearch);

    function handleSearch() {
        const query = searchInput.value;
    
        if (query === '') {
            // Si la búsqueda está vacía, simplemente muestra los productos seleccionados
            renderSelectedProducts();
        } else {
            // Realiza la solicitud AJAX y obtiene los datos de los productos
            fetch(`/products/search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    // Limpia los resultados anteriores
                    findsProductsContainer.innerHTML = '';
    
                    // Para cada producto en los resultados
                    data.products.forEach(product => {
                        // Crea un elemento HTML para el producto utilizando la función createProductElement
                        const productElement = createProductElement(product);
    
                        // Verifica si el producto estaba seleccionado previamente
                        const isSelected = selectedProducts.some(selectedProduct => {
                            const selectedProductId = selectedProduct.dataset.productId;

                            return parseInt(selectedProductId) === product.id;
                        });                        
                        if (isSelected) {
                            // Si estaba seleccionado previamente, marca el checkbox como seleccionado
                            const checkbox = productElement.querySelector('input[type="checkbox"]');
                            const quantitySearch = productElement.querySelector(`#cantidad-${product.id}`);

                            const quantity = document.getElementById(`quantity-${product.id}`);
                            var quantityParse = parseInt(quantity.textContent.match(/\d+/)[0]);

                            checkbox.checked = true;
                            quantitySearch.value = quantityParse;
                        }
    
                        // Agrega el elemento al contenedor de resultados
                        findsProductsContainer.appendChild(productElement);
                    });
    
                    // Agregar el evento click a todos los botones de cantidad
                    const quantityButtons = document.querySelectorAll('[data-type="plus"], [data-type="minus"]');
                    quantityButtons.forEach(button => {
                        button.addEventListener('click', handleQuantityButtonClick);
                    });
                })
                .catch(error => console.error(error));
        }
    }
    

    function renderSelectedProducts() {
        // Limpia los resultados anteriores en el contenedor de búsqueda
        findsProductsContainer.innerHTML = '';
        // Renderiza todos los productos seleccionados
        selectedProducts.forEach(productElement => {
            // Marca el checkbox como seleccionado
            const checkbox = productElement.querySelector('input[type="checkbox"]');
            checkbox.checked = true;

            // Agrega el elemento al contenedor de resultados
            findsProductsContainer.appendChild(productElement);
        });
    }

    function createSelectedProductElement(product, quantity) {
        const rowProduct = document.createElement('tr');
        rowProduct.classList.add('border-bottom');

        const headerrow = document.createElement('th');
        headerrow.classList.add('text-700', 'ps-0', 'pt-0');

        const divdetail = document.createElement('div');
        divdetail.classList.add('text-600', 'fw-normal', 'fs--2');
        divdetail.textContent = 'COD: '+ product.barcode;

        const buttonRemove = document.createElement('a');
        buttonRemove.classList.add('text-danger');
        buttonRemove.href = '#';
        buttonRemove.textContent = 'Quitar';
        buttonRemove.addEventListener('click', function () {
            removeProduct(rowProduct); // Llama a la función removeProduct pasando la fila del producto
            CalculateSubtotal();
          });

        const pricerow = document.createElement('th');
        pricerow.classList.add('pe-0', 'text-end', 'pt-0');
        var pricewithno = product.price.replace(/\$/g, "");
        pricerow.textContent = `$ ${parseFloat(pricewithno).toFixed(2)}`;

        headerrow.textContent = `${product.name}`;
        headerrow.appendChild(divdetail);
        headerrow.appendChild(buttonRemove);
        
        const quantityrow = document.createElement('th');
        quantityrow.classList.add('pe-0', 'text-end', 'pt-0');
        quantityrow.id = `quantity-${product.id}`;
        quantityrow.textContent = `(x${quantity})`;

        rowProduct.appendChild(headerrow);
        rowProduct.appendChild(quantityrow);
        rowProduct.appendChild(pricerow);

        rowProduct.dataset.productId = product.id;

        return rowProduct;
    }

    function createProductElement(product) {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product-item');
    
        const formCheckDiv = document.createElement('div');
        formCheckDiv.classList.add('form-check', 'mb-0', 'custom-radio', 'radio-select');
    
        // Checkboxes de los productos encontrados
        const inputElement = document.createElement('input');
        inputElement.classList.add('form-check-input');
        inputElement.id = product.id;
        inputElement.type = 'checkbox';
        inputElement.addEventListener('change', function () {
            const isChecked = inputElement.checked;
            if (isChecked) {
                const quantity = document.getElementById(`cantidad-${inputElement.id}`);

                // Si el checkbox se marca, agrega el producto a la lista de seleccionados
                const selectedProductElement = createSelectedProductElement(product, quantity.value);
                selectproductsContainer.appendChild(selectedProductElement);

                // Agregar el producto a la lista de productos seleccionados
                selectedProducts.push(productDiv);
            } else {
                // Si el checkbox se desmarca, elimina el producto de la lista de seleccionados si existe
                const selectedProductToRemove = document.querySelector(`[data-product-id="${product.id}"]`);

                if (selectedProductToRemove) {
                    selectedProductToRemove.remove();
                }
            }

            CalculateSubtotal();
        });
    
        const labelElement = document.createElement('label');
        labelElement.classList.add('form-check-label', 'mb-0', 'fw-bold', 'd-block');
        labelElement.htmlFor = product.id;
    
        const labelText = document.createTextNode(`${product.category} - ${product.brand}`);
        labelElement.appendChild(labelText);
    
        const radioSelectContent = document.createElement('span');
        radioSelectContent.classList.add('radio-select-content');
    
        const innerRow = document.createElement('div');
        innerRow.classList.add('row', 'gx-card', 'mx-0', 'bg-200', 'fs--1', 'fw-semi-bold');
    
        const leftColumn = document.createElement('div');
        leftColumn.classList.add('col-8', 'py-3', 'ps-1');
    
        const dFlexContainer = document.createElement('div');
        dFlexContainer.classList.add('d-flex', 'align-items-center');

        const productNameLink = document.createElement('h5');
        productNameLink.classList.add('fs-0');
    
        const productpatternH5 = document.createElement('div');
        productpatternH5.classList.add('flex-1');
        productpatternH5.appendChild(productNameLink);
    
        const productLink = document.createElement('a');
        productLink.classList.add('text-900');
        productLink.href = `/products/detail/product/${product.id}/`;
        const truncatedProductName = truncateString(product.name, 20);
        productLink.textContent = truncatedProductName;
    
        productNameLink.appendChild(productLink);
        productpatternH5.appendChild(productNameLink);
        dFlexContainer.appendChild(productpatternH5);
        leftColumn.appendChild(dFlexContainer);
    
        const rightColumn = document.createElement('div');
        rightColumn.classList.add('col-4', 'py-3', 'ps-1');

        const rowAlignItems = document.createElement('div');
        rowAlignItems.classList.add('row', 'align-items-center');

        const colMd8Container = document.createElement('div');
        colMd8Container.classList.add('col-md-8', 'd-flex', 'justify-content-end', 'justify-content-md-center', 'order-0');

        const inputGroup = document.createElement('div');
        inputGroup.classList.add('input-group', 'input-group-sm', 'flex-nowrap');
        inputGroup.setAttribute('data-quantity', 'data-quantity');

        const minusButton = document.createElement('button');
        minusButton.classList.add('btn', 'btn-sm', 'btn-outline-secondary', 'border-300', 'px-2');
        minusButton.setAttribute('data-type', 'minus');
        minusButton.setAttribute('data-prod-id', product.id);
        minusButton.textContent = '-';

        const quantityInput = document.createElement('input');
        quantityInput.classList.add('form-control', 'text-center', 'px-2', 'input-spin-none');
        quantityInput.type = 'number';
        quantityInput.min = '1';
        quantityInput.disabled = true;
        quantityInput.value = '1';
        quantityInput.setAttribute('aria-label', 'Amount (to the nearest dollar)');
        quantityInput.style.width = '50px';
        quantityInput.id = `cantidad-${product.id}`;

        const plusButton = document.createElement('button');
        plusButton.classList.add('btn', 'btn-sm', 'btn-outline-secondary', 'border-300', 'px-2');
        plusButton.setAttribute('data-type', 'plus');
        plusButton.setAttribute('data-prod-id', product.id);
        plusButton.textContent = '+';

        const colMd4 = document.createElement('div');
        colMd4.classList.add('col-md-4', 'text-end', 'ps-0', 'order-0', 'mb-2', 'mb-md-0', 'text-600');
        colMd4.id = `price-${product.id}`;
        colMd4.textContent = `$ ${product.price}`;

        inputGroup.appendChild(minusButton);
        inputGroup.appendChild(quantityInput);
        inputGroup.appendChild(plusButton);

        const divemptyclass = document.createElement('div');
        divemptyclass.appendChild(inputGroup)

        colMd8Container.appendChild(divemptyclass);

        rowAlignItems.appendChild(colMd8Container);
        rowAlignItems.appendChild(colMd4);

        rightColumn.appendChild(rowAlignItems);
   
        innerRow.appendChild(leftColumn);
        innerRow.appendChild(rightColumn);
        radioSelectContent.appendChild(innerRow);
        labelElement.appendChild(radioSelectContent);
        formCheckDiv.appendChild(inputElement);
        formCheckDiv.appendChild(labelElement);
        productDiv.appendChild(formCheckDiv);

        productDiv.dataset.productId = product.id;
    
        return productDiv;
    } 

    function removeProduct(listItem) {
        if (!listItem) {
            return; // Salir de la función si el elemento no existe
        }
        const productId = listItem.dataset.productId;
        const checkbox = document.getElementById(productId);
        listItem.parentElement.removeChild(listItem);
    
        // Busca y elimina el producto del array selectedProducts
        const selectedIndex = selectedProducts.findIndex(selectedProduct => selectedProduct.dataset.productId === productId);
        if (selectedIndex !== -1) {
            selectedProducts.splice(selectedIndex, 1);
        }
    
        if (checkbox) {
            checkbox.checked = false;
            checkbox.dispatchEvent(new Event('change')); // Dispara el evento 'change' para actualizar la lista
        }
    
        CalculateSubtotal();
    }
    
    function handleQuantityButtonClick(event) {
        const button = event.target;
        const type = button.getAttribute('data-type');
        const productId = button.getAttribute('data-prod-id');
        const inputElement = document.getElementById(`cantidad-${productId}`);
        
        if (type === 'plus') {
            // Incrementar el valor del input cuando se hace clic en el botón '+'
            inputElement.value = parseInt(inputElement.value, 10) + 1;
        } else if (type === 'minus') {
            // Decrementar el valor del input cuando se hace clic en el botón '-'
            const newValue = parseInt(inputElement.value, 10) - 1;
            // Asegurarse de que el valor no sea menor que 1
            inputElement.value = newValue >= 1 ? newValue : 1;
        }

        const quantity = document.getElementById(`quantity-${productId}`);
        quantity.textContent = `(x${inputElement.value})`;

        CalculateSubtotal();
    }

    function CalculateSubtotal() {
        // Obtén todos los checkboxes dentro del contenedor 'product-container'
        const checkboxes = document.querySelectorAll('#product-container input[type="checkbox"]');
        
        // Inicializa el subtotal en 0.00
        let subtotalValue = 0.00;
      
        // Recorre todos los checkboxes
        checkboxes.forEach(checkbox => {
          if (checkbox.checked) {
            // Si el checkbox está marcado, obtén el precio y la cantidad del producto relacionado
            const productId = checkbox.id;
            const precio = parseFloat(document.getElementById(`price-${productId}`).textContent.replace('$', ''));
            const cantidad = parseFloat(document.getElementById(`cantidad-${productId}`).value);
            
            // Calcula el subtotal para el producto y agrégalo al subtotal total
            const productoSubtotal = precio * cantidad;
            subtotalValue += productoSubtotal;
          }
        });
      
        // Formatea el valor del subtotal con dos decimales y actualiza el contenido del elemento 'subtotal'
        subtotalElement.textContent = `$ ${subtotalValue.toFixed(2)}`;

        // Acutaliza el Total
        updateTotal();
      }

    function updateTotal(){        
        var subtotal = parseFloat(subtotalElement.textContent.replace('$', '')).toFixed(2);
        var discount = parseFloat(discountElement.textContent.replace('$', '')).toFixed(2);
        var total = parseFloat(totalElement.textContent.replace('$', '')).toFixed(2);

        total = parseFloat(subtotal - discount).toFixed(2);
        totalElement.textContent = `$ ${total}`;
        TotalSuccess.textContent = `$ ${total}`;
    }
});
