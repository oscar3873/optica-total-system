document.addEventListener('DOMContentLoaded', () => {
    // Obtén el formulario de búsqueda y el contenedor de resultados de la tabla
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('table-purchase-body');

    // Agrega un evento de escucha al formulario para manejar la búsqueda AJAX
    searchForm.addEventListener('keyup', function (e) {
        e.preventDefault();
        const searchUrl = searchForm.getAttribute('data-ajax-search-url'); // URL para la búsqueda AJAX
        let searchTerm = searchInput.value.trim();

        // Verifica si el término de búsqueda contiene solo espacios en blanco
        if (searchTerm !== '' && searchTerm !== ' ') {
            // Hay término de búsqueda válido, se realiza la solicitud
            // Realiza la solicitud AJAX al backend para obtener los resultados
            $.ajax({
                url: searchUrl,
                data: { search_term: searchTerm },
                success: function (data) {
                    // Limpia los resultados anteriores
                    if (data.data.length > 0) {
                        searchResults.innerHTML = '';
                        data.data.forEach(function (promotion) {
                            const row = document.createElement('tr');
                            row.className = 'btn-reveal-trigger';

                            const nameCell = document.createElement('td');
                            nameCell.className = 'align-start name';
                            const nameText = document.createTextNode(promotion.name);
                            nameCell.appendChild(nameText);
                            row.appendChild(nameCell);

                            const type_promCell = document.createElement('td');
                            type_promCell.className = 'align-start type_prom';
                            const type_promText = document.createTextNode(promotion.type_prom);
                            type_promCell.appendChild(type_promText);
                            row.appendChild(type_promCell);

                            const start_dateCell = document.createElement('td');
                            start_dateCell.className = 'align-start start_date d-none d-md-table-cell';
                            const start_dateText = document.createTextNode(promotion.start_date);
                            start_dateCell.appendChild(start_dateText);
                            row.appendChild(start_dateCell);

                            const end_dateCell = document.createElement('td');
                            end_dateCell.className = 'align-start end_date d-none d-md-table-cell';
                            const end_dateText = document.createTextNode(promotion.end_date);
                            end_dateCell.appendChild(end_dateText);
                            row.appendChild(end_dateCell);

                            const is_activeCell = document.createElement('td');
                            is_activeCell.className = 'align-start is_active';
                            const is_activeSpan = document.createElement('span');
                            let is_activeText;
                            if(promotion.is_active){
                                is_activeSpan.className = 'badge badge-soft-success rounded-pill';
                                is_activeText = document.createTextNode('Activa');
                            }
                            else{
                                is_activeSpan.className = 'badge badge-soft-secondary rounded-pill';
                                is_activeText = document.createTextNode('Inactiva');
                            }
                            pricespan.appendChild(is_activeText);
                            priceCell.appendChild(is_activeSpan);
                            row.appendChild(is_activeCell);

                            const actionsCell = document.createElement('td');
                            actionsCell.className = 'align-middle white-space-nowrap text-start';
                            
                            const actionsDropdown = document.createElement('div');
                            actionsDropdown.className = 'dropstart font-sans-serif position-static d-inline-block';

                            const actionsButton = document.createElement('button');
                            actionsButton.className = 'btn btn-link text-600 btn-sm dropdown-toggle btn-reveal float-end';
                            actionsButton.type = 'button';
                            actionsButton.id = 'dropdown0';
                            actionsButton.setAttribute('data-bs-toggle', 'dropdown');
                            actionsButton.setAttribute('data-boundary', 'window');
                            actionsButton.setAttribute('aria-haspopup', 'true');
                            actionsButton.setAttribute('aria-expanded', 'false');
                            actionsButton.setAttribute('data-bs-reference', 'parent');
                            const actionsIcon = document.createElement('span');
                            actionsIcon.className = 'fas fa-ellipsis-h fs--1';
                            actionsButton.appendChild(actionsIcon);

                            const dropdownMenu = document.createElement('div');
                            dropdownMenu.className = 'dropdown-menu dropdown-menu-end border py-2';
                            dropdownMenu.setAttribute('aria-labelledby', 'dropdown0');

                            const detailLink = document.createElement('a');
                            detailLink.className = 'dropdown-item';
                            detailLink.href = `/products/detail/product/${product.id}`;
                            detailLink.textContent = 'Detalle';
                            dropdownMenu.appendChild(detailLink);
                            if (product.is_staff) {
                                const editLink = document.createElement('a');
                                editLink.className = 'dropdown-item';
                                editLink.href = `/promotions/update/${product.id}`;
                                editLink.textContent = 'Editar';
                                dropdownMenu.appendChild(editLink);

                                const divider = document.createElement('div');
                                divider.className = 'dropdown-divider';
                                dropdownMenu.appendChild(divider);

                                const deleteLink = document.createElement('a');
                                deleteLink.className = 'dropdown-item text-danger';
                                deleteLink.href = `/promotions/delete/promotion/${product.id}`;
                                deleteLink.textContent = 'Borrar';
                                dropdownMenu.appendChild(deleteLink);
                            }

                            actionsDropdown.appendChild(actionsButton);
                            actionsDropdown.appendChild(dropdownMenu);
                            actionsCell.appendChild(actionsDropdown);
                            row.appendChild(actionsCell);

                            searchResults.appendChild(row);
                        });

                    } else {
                        // Mostrar un mensaje si no se encuentran resultados
                        searchResults.innerHTML = '<tr><td colspan="5">No se encontraron resultados</td></tr>';
                    }

                },
                error: function (error) {
                    console.error('Error al realizar la búsqueda:', error);
                    searchResults.innerHTML = '<tr><td colspan="5">Error al realizar la búsqueda</td></tr>';
                },
            });
        }
    });
});