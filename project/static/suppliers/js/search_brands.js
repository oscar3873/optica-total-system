document.addEventListener("DOMContentLoaded", function () {
    function configureSearch(searchInput, searchResults) {
        searchInput.addEventListener('input', (event) => {
            const searchTerm = event.target.value.trim().toLowerCase();

            if (!searchTerm) {
                // Limpiar los resultados de búsqueda si no hay término de búsqueda
                searchResults.innerHTML = '';
                return;
            }

            // Realizar la búsqueda de marcas que coincidan con el término de búsqueda
            $.ajax({
                url: `/suppliers/brands/ajax_search_brands/?search_term=${searchTerm}`,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    const brands = data.data;

                    // Mostrar los resultados de búsqueda
                    searchResults.innerHTML = ''; // Limpia los resultados anteriores

                    brands.forEach(brand => {
                        const item = document.createElement('li');
                        item.style.zIndex = "3";
                        item.style.cursor = 'pointer';
                        item.classList.add('list-group-item', 'brands', 'list-group-item-secondary');
                        item.dataset.brandId = brand.id;
                        item.textContent = brand.name;
                        searchResults.appendChild(item);
                    });
                },
                error: function(error) {
                    console.error('Error en la solicitud AJAX', error);
                }
            });
        });

        searchResults.addEventListener('click', (event) => {
            const item = event.target.closest('.brands');
            if (!item) {
                return;
            }

            const brandId = item.dataset.brandId;
            const brandName = item.textContent;

            // Rellenar el campo de la marca seleccionada y ocultar los resultados de búsqueda
            searchInput.value = '';
            searchResults.innerHTML = '';

            // Aquí puedes realizar las acciones que desees con la marca seleccionada, como agregarla a una lista, etc.
        });
    }

    // Configura el buscador de marcas
    const searchInputBrands = document.getElementById('id_brands-search');
    const searchResultsBrands = document.getElementById('id_brands-search-results');
    configureSearch(searchInputBrands, searchResultsBrands);
});
