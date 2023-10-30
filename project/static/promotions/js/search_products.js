let idProductGlobal;
let setProductIds = new Set();
document.addEventListener("DOMContentLoaded", function () {
    const checkboxContainer = document.getElementById('products-selected');
    if(checkboxContainer.classList.contains('update')){
        const checkboxes = Array.from(checkboxContainer.querySelectorAll('input[type="checkbox"]'));
        checkboxes.forEach(checkbox => {
            setProductIds.add(parseInt(checkbox.value));
        });
    }
    function configureSearch(searchInput, searchResults, fieldIdentifier) {
        searchInput.addEventListener('input', (event) => {
            const searchTerm = event.target.value.trim().toLowerCase();

            if (!searchTerm) {
                // Limpiar los resultados de búsqueda si no hay término de búsqueda
                searchResults.innerHTML = '';
                return;
            }

            // Realizar la búsqueda de productos que coincidan con el término de búsqueda
            $.ajax({
                url: `/products/ajax_search_products/?search_term=${searchTerm}`,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    const products = data.data;

                    // Mostrar los resultados de búsqueda
                    searchResults.innerHTML = ''; // Limpia los resultados anteriores

                    products.forEach(product => {
                        if(!setProductIds.has(product.id) && !product.in_promo){
                            const item = document.createElement('li');
                            item.style.zIndex = "3";
                            item.style.cursor = 'pointer';
                            item.classList.add('list-group-item', 'products', 'list-group-item-secondary');
                            item.dataset.productId = product.id;
                            item.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <h6>${product.name}</h6>
                                <h6 class="font-weight-bold">&nbsp${product.barcode}</h6>
                            </div>
                        `;
                        searchResults.appendChild(item);
                        };
                        
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
            idProductGlobal=productId;
            const productName = item.querySelector('h6').textContent;

            // Rellenar el campo del producto seleccionado y ocultar los resultados de búsqueda
            searchInput.value = '';
            searchResults.innerHTML = '';

            const checkboxProduct = document.createElement("input");
            checkboxProduct.type = "checkbox";
            checkboxProduct.classList.add('form-check-input');
            // Asegúrate de que todas las casillas de verificación tengan el mismo nombre
            checkboxProduct.name = "productsSelected"; 
            checkboxProduct.value = productId;
            checkboxProduct.id = `${productName}`;
            checkboxProduct.checked = true;
            const label = document.createElement("label");
            label.textContent = productName;
            label.classList.add('d-block');


            
            label.appendChild(checkboxProduct);
            checkboxContainer.appendChild(label);

            checkboxProduct.addEventListener("change", function () {
                if (!checkboxProduct.checked) {
                    // Si el checkbox se desmarca, elimina el checkbox y su etiqueta
                    checkboxContainer.removeChild(label);
                    setProductIds.delete(parseInt(checkboxProduct.value));    
                }
            });

            setProductIds.add(parseInt(productId));
            // Añadir el ID del producto al formulario
            const productIdCheck = document.createElement('input');
            productIdCheck.type = 'hidden';
            productIdCheck.name = `selected_product_id_${fieldIdentifier}`;
            productIdCheck.value = productId;
            searchInput.closest('form').appendChild(productIdCheck);
        });
    }


    function configureSearchInputs(form, count) {
        const fieldPrefix = `id_form-${count}`;
        const searchInputA = form.querySelector(`#${fieldPrefix}-search-productA-input`);
        const searchResultsA = form.querySelector(`#${fieldPrefix}-search-productA-results`);
        configureSearch(searchInputA, searchResultsA, 'productA');
    }


    // SOLO PARA EL FORMULARIO 1
    const form_0 = document.getElementById('id_form-0');
    configureSearchInputs(form_0, 0);
});
