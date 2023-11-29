let idProductGlobal;
let setProductIds = new Set();
let itemClicked = false;
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
                
                // url: `/products/ajax_search_products/?search_term=${searchTerm}`,
                url: `/products/search-categories-or-brands/?search_term=${searchTerm}`,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    //Data es un array de resultados de la busqueda de nombres de marcas y categorias
                    console.log(data);
                    

                    // Mostrar los resultados de búsqueda
                    searchResults.innerHTML = ''; // Limpia los resultados anteriores
                    

                    data.forEach(item => {
                        const element = document.createElement('li');
                        element.style.zIndex = "3";
                        element.style.cursor = 'pointer';
                        element.classList.add('list-group-item','searchType', 'list-group-item-secondary');
                        element.dataset.itemId = item.id;
                        element.setAttribute('name',`${item.name}`);
                        let type;
                        if(item.form_name == 'brand'){
                            type = 'Marca:';
                        }else{
                            type = 'Categoría:';
                        }
                        element.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <h6>${type} ${item.name}</h6>
                        </div>
                        `;

                        // element.addEventListener('click', function () {
                        //     itemClicked=true;
                        //     console.log('hizo click en el elemento');
                        // });
                        searchResults.appendChild(element);
                    });
                },
                error: function(error) {
                    console.error('Error en la solicitud AJAX', error);
                }
            });
        });

        searchResults.addEventListener('click', (event) => {

            const item = event.target.closest('.searchType');
            if (!item) {
                return;
            }

            $.ajax({
                url: `/products/ajax-search-products/?search_term=${item.getAttribute('name')}`,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    const products = data.data;
                    products.forEach(product => {
                        if(!setProductIds.has(product.id)){
                            const productId = product.id;
                            idProductGlobal=product.id;
                            const productName = product.name;
                            const checkboxProduct = document.createElement("input");
                            checkboxProduct.type = "checkbox";
                            checkboxProduct.classList.add('form-check-input');
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
                            
                        }
                        

                    });
                },
                error: function(error) {
                    console.error('Error en la solicitud AJAX', error);
                }
            });

            // Rellenar el input y ocultar los resultados de búsqueda
            searchInput.value = item.getAttribute('name');
            searchResults.innerHTML = '';

            
        });
    }


    function configureSearchInputs(form, count) {
        const fieldPrefix = `id_form-${count}`;
        const searchInputA = form.querySelector(`#${fieldPrefix}-search-productA-input`);
        const searchResultsA = form.querySelector(`#${fieldPrefix}-search-productA-results`);
        configureSearch(searchInputA, searchResultsA, 'productA');
        //evento para limpiar la lista cuando se hace click en otro lugar
        // searchInputA.addEventListener("blur", function(item) {
        //     if(!itemClicked){
        //         searchInputA.value = "";
        //         searchResultsA.innerHTML = '';
        //         itemClicked=false;
        //     }
        //     else{
        //         itemClicked=false;
        //     }
            
        // });
    }


    // SOLO PARA EL FORMULARIO 1
    const form_0 = document.getElementById('id_form-0');
    configureSearchInputs(form_0, 0);
});
