let setBrandsSelected = new Set();

document.addEventListener("DOMContentLoaded", function () {
    function configureSearch(searchInput, searchResults) {
        searchInput.addEventListener('input', (event) => {
            let searchTerm = event.target.value.trim().toLowerCase();

            if (!searchTerm) {
                // Limpiar los resultados de búsqueda si no hay término de búsqueda
                searchResults.innerHTML = '';
                return;
            }

            // Realizar la búsqueda de marcas que coincidan con el término de búsqueda
            $.ajax({
                url: `/suppliers/brands/ajax-search-brands/`,
                dataType: 'json',
                success: function(data) {
                    const brands = data.data;

                    // Mostrar los resultados de búsqueda
                    searchResults.innerHTML = ''; // Limpia los resultados anteriores
                    
                    brands.forEach(brand => {
                        if(!setBrandsSelected.has(brand.id)){
                            const item = document.createElement('li');
                            item.style.zIndex = "3";
                            item.style.cursor = 'pointer';
                            item.classList.add('list-group-item', 'brands', 'list-group-item-secondary');
                            item.dataset.brandId = brand.id;
                            item.textContent = brand.name;

                            item.addEventListener('click', function () {
                                createCheckbox(brand.name, brand.id)
                            });
                            searchResults.appendChild(item);
                        }
                    });
                },
                error: function(error) {
                    console.error('Error en la solicitud AJAX', error);
                }
            });
        });

        searchResults.addEventListener('click', () => {
            //limpiar el input de busqueda y ocultar los resultados de búsqueda
            searchInput.value = '';
            searchResults.innerHTML = '';
        });

        
    }

    // Configura el buscador de marcas
    const searchInputBrands = document.getElementById('id_brands-search');
    const searchResultsBrands = document.getElementById('id_brands-search-results');
    configureSearch(searchInputBrands, searchResultsBrands);
});


function createCheckbox(name, itemId){
    const checkboxContainer = document.getElementById('brands-selected');
    setBrandsSelected.add(parseInt(itemId));

    const checkboxProduct = document.createElement("input");
    checkboxProduct.type = "checkbox";
    checkboxProduct.classList.add('form-check-input');
    checkboxProduct.name = "brandsSelected"; 
    checkboxProduct.value = itemId;
    checkboxProduct.id = `${name}`;
    checkboxProduct.checked = true;
    const label = document.createElement("label");
    label.textContent = name;
    label.classList.add('d-block');
    label.appendChild(checkboxProduct);
    checkboxContainer.appendChild(label);
    checkboxProduct.addEventListener("change", function () {
        if (!checkboxProduct.checked) {
            // Si el checkbox se desmarca, elimina el checkbox y su etiqueta
            checkboxContainer.removeChild(label);
            setBrandsSelected.delete(parseInt(checkboxProduct.value));    
        }
    });


};

