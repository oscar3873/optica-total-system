document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-product');
    const searchResults = document.getElementById('product-container');

    function handleSearch() {
        const query = searchInput.value; // Obtiene la consulta de búsqueda
        
        if (query === '') {
            // Si la búsqueda está vacía, elimina los productos que se mostraron previamente
            const productContainer = document.getElementById('product-container');
            productContainer.innerHTML = 'Aqui veras los productos de la busqueda.'; // Borra todo el contenido dentro del contenedor
        } else {
            // Realiza la solicitud AJAX y obtiene los datos de los productos
            fetch(`/products/search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    // Limpia los resultados anteriores
                    searchResults.innerHTML = '';
        
                    // Para cada producto en los resultados
                    data.products.forEach(product => {
                        // Crea un elemento HTML para el producto utilizando la función createProductElement
                        const productElement = createProductElement(product);
        
                        // Agrega el elemento al contenedor de resultados
                        searchResults.appendChild(productElement);
                    });
                    // Agregar el evento click a todos los botones de cantidad
                    const quantityButtons = document.querySelectorAll('[data-type="plus"], [data-type="minus"]');
                    quantityButtons.forEach(button => {
                        console.log('asdasdas');
                        button.addEventListener('click', handleQuantityButtonClick);
                    });
                })
                .catch(error => console.error(error));
        }
    }
    
    // Event listener para el campo de búsqueda
    searchInput.addEventListener('input', handleSearch);

    function createProductElement(product) {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product-item');
    
        const formCheckDiv = document.createElement('div');
        formCheckDiv.classList.add('form-check', 'mb-0', 'custom-radio', 'radio-select');
    
        const inputElement = document.createElement('input');
        inputElement.classList.add('form-check-input');
        inputElement.id = product.id;
        inputElement.type = 'checkbox';
    
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
        productLink.textContent = product.name;
    
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
        minusButton.setAttribute('data-product-id', product.id);
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
        plusButton.setAttribute('data-product-id', product.id);
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
    
        return productDiv;
    }   
    
    function handleQuantityButtonClick(event) {
        const button = event.target;
        const type = button.getAttribute('data-type');
        const productId = button.getAttribute('data-product-id');
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
    }

});
