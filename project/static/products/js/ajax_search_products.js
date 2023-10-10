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
                        data.data.forEach(function (product) {
                            console.log(product);
                            const row = document.createElement('tr');
                            row.className = 'btn-reveal-trigger';

                            const nameCell = document.createElement('td');
                            nameCell.className = 'align-start name';
                            const nameText = document.createTextNode(product.name);
                            nameCell.appendChild(nameText);
                            row.appendChild(nameCell);

                            const barcodeCell = document.createElement('td');
                            barcodeCell.className = 'align-start barcode';
                            const barcodeText = document.createTextNode(product.barcode);
                            barcodeCell.appendChild(barcodeText);
                            row.appendChild(barcodeCell);

                            const priceCell = document.createElement('td');
                            priceCell.className = 'align-start sell_price d-none d-md-table-cell';
                            const priceText = document.createTextNode(product.sale_price);
                            priceCell.appendChild(priceText);
                            row.appendChild(priceCell);

                            const descriptionCell = document.createElement('td');
                            descriptionCell.className = 'align-start description d-none d-md-table-cell';
                            const descriptionText = document.createTextNode(product.description);
                            descriptionCell.appendChild(descriptionText);
                            row.appendChild(descriptionCell);

                            const stockCell = document.createElement('td');
                            stockCell.className = 'align-start stock d-none d-md-table-cell';
                            const stockText = document.createTextNode(product.stock);
                            stockCell.appendChild(stockText);
                            row.appendChild(stockCell);

                            const categoryCell = document.createElement('td');
                            categoryCell.className = 'align-start category d-none d-md-table-cell';
                            const categoryText = document.createTextNode(product.category);
                            categoryCell.appendChild(categoryText);
                            row.appendChild(categoryCell);

                            const brandCell = document.createElement('td');
                            brandCell.className = 'align-start brand d-none d-md-table-cell';
                            const brandText = document.createTextNode(product.brand);
                            brandCell.appendChild(brandText);
                            row.appendChild(brandCell);

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
                            console.log(`Es staff ${product.is_staff}`)
                            if (product.is_staff) {
                                const editLink = document.createElement('a');
                                editLink.className = 'dropdown-item';
                                editLink.href = `/products/update/${product.id}`;
                                editLink.textContent = 'Editar';
                                dropdownMenu.appendChild(editLink);

                                const divider = document.createElement('div');
                                divider.className = 'dropdown-divider';
                                dropdownMenu.appendChild(divider);

                                const deleteLink = document.createElement('a');
                                deleteLink.className = 'dropdown-item text-danger';
                                deleteLink.href = `/products/delete/product/${product.id}`;
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