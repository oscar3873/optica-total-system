function configureSearch(searchInput, searchResults, fieldIdentifier) {
    searchInput.addEventListener('input', (event) => {
        const searchTerm = event.target.value.trim().toLowerCase();

        if (!searchTerm) {
            // Limpiar los resultados de búsqueda si no hay término de búsqueda
            searchResults.innerHTML = '';
            return;
        }

        // Realizar la búsqueda de products que coincidan con el término de búsqueda
        $.ajax({
            url: `/products/ajax_search_products/?search_term=${searchTerm}`,
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                const products = data.data;

                // Mostrar los resultados de búsqueda
                searchResults.innerHTML = ''; // Limpia los resultados anteriores

                products.forEach(product => {
                    const item = document.createElement('li');
                    item.style.zIndex = "9999";
                    item.style.cursor = 'pointer';
                    item.classList.add('list-group-item', 'products');
                    item.dataset.productId = product.id;
                    item.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <h6>${product.name}</h6>
                            <h6 class="font-weight-bold">&nbsp${product.barcode}</h6>
                        </div>
                    `;
                    searchResults.appendChild(item);
                });
            },
            error: function(error) {
                console.error('Error en la solicitud AJAX', error);
            }
        });
    });

    searchResults.addEventListener('click', (event) => {
        const item = event.target.closest('.products');
        if (!item) {
            return;
        }

        const productId = item.dataset.productId;
        const productName = item.querySelector('h6').textContent;

        // Rellenar el campo del product seleccionado y ocultar los resultados de búsqueda
        searchInput.value = productName;
        searchResults.innerHTML = '';
        // Añadir el id del product al formulario
        const productIdCheck = document.createElement('checkbox');
        productIdCheck.type = 'hidden';
        productIdCheck.value = productId;
        searchInput.closest('form').appendChild(productIdCheck);
    });
}

// Configurar el buscador A
const searchInputA = document.getElementById('id_form-0-search-productA-input');
const searchResultsA = document.getElementById('id_form-0-search-productA-results');
configureSearch(searchInputA, searchResultsA, 'productA');

// Configurar el buscador B
const searchInputB = document.getElementById('id_form-0-search-productB-input');
const searchResultsB = document.getElementById('id_form-0-search-productB-results');
configureSearch(searchInputB, searchResultsB, 'productB');
