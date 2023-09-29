document.addEventListener('DOMContentLoaded', function() {

    // cuando el usuario hace clic en el botón "add more" de las variantes
    function addFormset(product) {
        const form = $('#selected-products-list').children()
        var count = form.length;
        var itemVariants = document.getElementById('selected-products-list');
        
        const rowProduct = document.createElement('tr');
        rowProduct.id = `order_detaill-formset-${product.id}`
        rowProduct.classList.add('border-bottom');
    
        const headerrow = document.createElement('th');
        headerrow.classList.add('fs-1', 'col-8', 'text-700', 'px-0', 'pt-0');
        headerrow.textContent = product.name;
    
        const divdetail = document.createElement('div');
        divdetail.classList.add('text-600', 'fw-normal', 'fs--1');
        divdetail.textContent = 'COD: ' + product.barcode;
    
        const buttonRemove = document.createElement('a');
        buttonRemove.classList.add('text-danger');
        buttonRemove.href = '#';
        buttonRemove.textContent = 'Quitar';
        buttonRemove.addEventListener('click', function () {
            removeProduct(product.id); // Llama a la función removeProduct pasando la fila del producto
        });
    
        const pricerow = document.createElement('th');
        pricerow.classList.add('fs-1', 'px-0', 'text-end', 'pt-0');
        var pricewithno = product.price.replace(/\$/g, "");
        pricerow.textContent = `$ ${parseFloat(pricewithno).toFixed(2)}`;

        const checkbox_form = document.createElement('input');
        checkbox_form.type = 'checkbox';
        checkbox_form.name = `order_detaill-${count}-product`;
        checkbox_form.value = product.id;
        checkbox_form.checked = true;
        checkbox_form.hidden = true;

        const quantityRowcontainer = document.createElement('div');
        quantityRowcontainer.classList.add('my-3', 'col-8', 'col-sm-6', 'col-md-5', 'col-xl-8');
    
        const quantityRow = document.createElement('div');
        quantityRow.classList.add('input-group', 'input-group-sm', 'flex-nowrap');
        
        // Crear botones de cantidad
        const minusButton = document.createElement('button');
        minusButton.classList.add('btn', 'btn-sm', 'btn-outline-secondary', 'border-300','px-3', 'py-2', 'btn-fixed-size'); 
        minusButton.setAttribute('data-type', 'minus');
        minusButton.setAttribute('data-prod-id', product.id);
        minusButton.textContent = '-';
        minusButton.type = 'button';
        minusButton.addEventListener('click', handleQuantityButtonClick);
        
        // const quantity_variant = quantity_orginal.cloneNode();
        const quantity_variant = document.createElement('input');
        quantity_variant.classList.add('form-control', 'text-center', 'px-2', 'input-spin-none', 'input-fixed-size');
        quantity_variant.type = 'number';
        quantity_variant.min = '1';
        quantity_variant.readonly = true;
        quantity_variant.value = 1;
        quantity_variant.id = `id_order_detaill-${product.id}-quantity`;
        quantity_variant.name = `order_detaill-${count}-quantity`;
        
        
        const plusButton = document.createElement('button');
        plusButton.classList.add('btn', 'btn-sm', 'btn-outline-secondary', 'border-300','px-3', 'py-2', 'btn-fixed-size');
        plusButton.setAttribute('data-type', 'plus');
        plusButton.setAttribute('data-prod-id', product.id);
        plusButton.textContent = '+';
        plusButton.type = 'button';
        plusButton.addEventListener('click', handleQuantityButtonClick);
        
        quantityRow.appendChild(minusButton);
        quantityRow.appendChild(quantity_variant);
        quantityRow.appendChild(plusButton);
    
        quantityRowcontainer.appendChild(quantityRow);

        headerrow.appendChild(divdetail);
        headerrow.appendChild(checkbox_form);
        headerrow.appendChild(quantityRowcontainer);
        headerrow.appendChild(buttonRemove);

        rowProduct.appendChild(headerrow);
        rowProduct.appendChild(pricerow);
    
        rowProduct.dataset.productId = product.id;


        itemVariants.appendChild(rowProduct);

        // actualizar el contador de formularios
        var totalForms = document.getElementById('id_order_detaill-TOTAL_FORMS');
        totalForms.value = count + 1;

        return rowProduct;
    };

    const searchInput = document.getElementById('search-product');
    const findsProductsContainer = document.getElementById('product-container');
    const selectproductsContainer = document.getElementById('selected-products-list'); 
    const subtotalElement = document.getElementById('subtotal');

    const totalElement = document.getElementById('total');
    const discountElement = document.getElementById('discount');
    const TotalSuccess = document.getElementById('total-success');

    const ButtonDelete = document.getElementById("button-delete-all");
    ButtonDelete.addEventListener('click', function() {
        const productIds = [...selectproductsContainer.querySelectorAll('tr')]
            .map(tr => tr.getAttribute('data-product-id'))
            .filter(productId => productId);
        // Llama a removeProduto con cada id
        productIds.forEach(productId => removeProduct(productId));
    });


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
            findsProductsContainer.innerHTML = 'Aqui veras los productos de la busqueda.';
        } else {
            // Realiza la solicitud AJAX y obtiene los datos de los productos
            fetch(`/products/search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    if (data.products.length === 0) {
                        findsProductsContainer.innerHTML = 'No se ha encontrado coincidencias.';
                    } else {
                        // Limpia los resultados anteriores
                        findsProductsContainer.innerHTML = '';
        
                        // Para cada producto en los resultados
                        data.products.forEach(product => {
                            // Crea un elemento HTML para el producto utilizando la función createProductElement
                            const productElement = createProductElement(product);
        
                            // Verifica si el producto estaba seleccionado previamente
                            selectedProducts.some(selectedProduct => {
                                const selectedProductId = selectedProduct.dataset.productId;
                            
                                if (parseInt(selectedProductId) === product.id) {
                                    // Si estaba seleccionado previamente, marca el checkbox como seleccionado
                                    const checkbox = productElement.querySelector('input[type="checkbox"]');
                                    checkbox.checked = true;
                                }
                            });
                            // Agrega el elemento al contenedor de resultados
                            findsProductsContainer.appendChild(productElement);
                        });
                    }
                })
                .catch(error => console.error(error));
        }
    }

    function createProductElement(product) {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product-item');
    
        const formCheckDiv = document.createElement('div');
        formCheckDiv.classList.add('form-check', 'mb-0', 'custom-radio', 'radio-select', 'ps-0');
    
        // Checkboxes de los productos encontrados
        const inputElement = document.createElement('input');
        inputElement.classList.add('form-check-input');
        inputElement.id = product.id;
        inputElement.type = 'checkbox';
        inputElement.name = 'products';
        inputElement.value = product.id;
        inputElement.addEventListener('change', function () {
            const isChecked = inputElement.checked;
            if (isChecked) {
                addFormset(product);

                // Agregar el producto a la lista de productos seleccionados
                selectedProducts.push(productDiv);
            } else {
                // Elimina el formset generado con la id del producto
                removeProduct(product.id);
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

        const barcode = document.createElement('div');
        barcode.classList.add('fs--1', 'text-500');
        barcode.textContent = 'COD: '+ product.barcode;
    
        const productpatternH5 = document.createElement('div');
        productpatternH5.classList.add('flex-1');
        
    
        const productLink = document.createElement('a');
        productLink.classList.add('text-900');
        productLink.href = `/products/detail/product/${product.id}/`;
        const truncatedProductName = truncateString(product.name, 20);
        productLink.textContent = truncatedProductName;
    
        productNameLink.appendChild(productLink);
        productpatternH5.appendChild(productNameLink);
        productpatternH5.appendChild(barcode);
        dFlexContainer.appendChild(productpatternH5);
        leftColumn.appendChild(dFlexContainer);
    
        const rightColumn = document.createElement('div');
        rightColumn.classList.add('col-4', 'py-3', 'ps-1');

        const colMd4 = document.createElement('div');
        colMd4.classList.add('fs-1', 'text-end', 'ps-0', 'order-0', 'mb-2', 'mb-md-0', 'text-600');
        colMd4.id = `price-${product.id}`;
        colMd4.textContent = `$ ${product.price}`;

        rightColumn.appendChild(colMd4);
   
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

    function reorderFormNames() {
        var forms = $('#selected-products-list').children();

        forms.each(function(i) {
            $(this).find('input').each(function() {
                const [, number, fieldName] = $(this).attr('name').match(/^order_detaill-(\d+)-(product|quantity)$/);
                if (number && fieldName) {
                    $(this).attr('name', `order_detaill-${i}-${fieldName}`);
                }
            });
        });
    }    

    function removeProduct(productId) {
        if (!productId) {
            return; // Salir de la función si el elemento no existe
        }
        const checkbox = document.getElementById(productId);
    
        // Busca y elimina el producto del array selectedProducts
        const indexToRemove = selectedProducts.findIndex(product => product.dataset.productId == productId);

        if (indexToRemove !== -1) {
            selectedProducts.splice(indexToRemove, 1);
        }
    
        // Si el checkbox se desmarca, elimina el producto de la lista de seleccionados si existe
        const selectedProductToRemove = document.querySelector(`[data-product-id="${productId}"]`);
        if (selectedProductToRemove) {
            selectedProductToRemove.remove();
        }

        if (checkbox && checkbox.checked) {
            checkbox.checked = false;
            // checkbox.dispatchEvent(new Event('change')); // Dispara el evento 'change' para actualizar la lista
        }

        // actualizar el contador de formularios
        var totalForms = document.getElementById('id_order_detaill-TOTAL_FORMS');
        totalForms.value = parseInt(totalForms.value) - 1;

        reorderFormNames();

        CalculateSubtotal();
    }
    
    function handleQuantityButtonClick(event) {
        const button = event.target;
        const type = button.getAttribute('data-type');
        const productId = button.getAttribute('data-prod-id');
        const inputElement = document.querySelector(`[id="id_order_detaill-${productId}-quantity"]`);
    
        if (type === 'plus') {
            inputElement.value = parseInt(inputElement.value, 10) + 1;
        } else if (type === 'minus') {
            const newValue = parseInt(inputElement.value, 10) - 1;
            inputElement.value = newValue >= 1 ? newValue : 1;
        }
        
        const selectedProductonList = findsProductsContainer.querySelector(`[id="id_order_detaill-${productId}-quantity"]`);
        if (selectedProductonList){
            selectedProductonList.value = inputElement.value
        }

        const selectedProduct = selectedProducts.find(product => product.dataset.productId === productId);
        if (selectedProduct) {
            const cantidadElement = selectedProduct.querySelector(`[id="id_order_detaill-${productId}-quantity"]`);
            if (cantidadElement) {
                cantidadElement.value = inputElement.value;
            }
        }
        
        CalculateSubtotal();
    }

    function CalculateSubtotal() {
        const checkboxes = document.querySelectorAll('#product-container input[type="checkbox"]');

        let subtotalValue = 0.00;
      
        checkboxes.forEach(checkbox => {
          if (checkbox.checked) {
            // Si el checkbox está marcado, obtén el precio y la cantidad del producto relacionado
            const productId = checkbox.id;
            const precio = parseFloat(document.getElementById(`price-${productId}`).textContent.replace('$', ''));
            const cantidad = parseFloat(document.getElementById(`id_order_detaill-${productId}-quantity`).value);
            
            // Calcula el subtotal para el producto y agrégalo al subtotal total
            const productoSubtotal = precio * cantidad;
            subtotalValue += productoSubtotal;
          }
        });
      
        subtotalElement.textContent = `$ ${subtotalValue.toFixed(2)}`;

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
