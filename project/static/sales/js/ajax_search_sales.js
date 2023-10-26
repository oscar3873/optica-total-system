document.addEventListener('DOMContentLoaded', () => {
    //Para poder ponerle un pequeño delay
    let timeoutId;

    //loader para los movimientos
    // const loader = document.getElementById('loader-sales');

    // Obtén el formulario de búsqueda y el contenedor de resultados de la tabla
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('table-purchase-body');

    // Agrega un evento de escucha al formulario para manejar la búsqueda AJAX
    searchForm.addEventListener('input', function (e) {

        //Se borra el temporizador anterior (si es que existe)
        clearTimeout(timeoutId);
        // loader.classList.remove('d-none');
        // Establece un nuevo temporizador para retrasar la solicitud
        timeoutId = setTimeout(function () {
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
                            data.data.forEach(function (sale) {
                                const row = document.createElement('tr');
                                row.className = 'btn-reveal-trigger';
                                //User made
                                const nameCell = document.createElement('td');
                                nameCell.className = 'align-start user_made d-none d-sm-table-cell';
                                const nameText = document.createTextNode(sale.user_made);
                                nameCell.appendChild(nameText);
                                row.appendChild(nameCell);
                                //Fecha
                                const dateSaleCell = document.createElement('td');
                                dateSaleCell.className = 'align-start date_time_sale d-none d-sm-table-cell';
                                const descriptionText = document.createTextNode(sale.date_time_sale);
                                dateSaleCell.appendChild(descriptionText);
                                row.appendChild(dateSaleCell);
                                //Cliente
                                const clientCell = document.createElement('td');
                                clientCell.className = 'align-start customer';
                                const clientText = document.createTextNode(sale.customer);
                                const clientLink = document.createElement('a');
                                clientLink.href = `/customers/detail/${sale.customer_id}`;
                                clientLink.appendChild(clientText);
                                clientCell.appendChild(clientLink);
                                row.appendChild(clientCell);
                                //Estado
                                const stateCell = document.createElement('td');
                                stateCell.className = 'align-start state';
                                const stateSpan = document.createElement('span');
                                stateSpan.className = sale.state === 'COMPLETADO'?'badge rounded-pill badge-soft-success': 'badge rounded-pill badge-soft-secondary';
                                const stateText = document.createTextNode(`${sale.state}`);
                                stateSpan.appendChild(stateText);
                                stateCell.appendChild(stateSpan);
                                row.appendChild(stateCell);
                                //Saldo
                                const missingBalanceCell = document.createElement('td');
                                missingBalanceCell.className = 'align-start missing_balance';
                                const missingBalance = document.createTextNode(sale.missing_balance);
                                missingBalanceCell.appendChild(missingBalance);
                                row.appendChild(missingBalanceCell);
                                //Total
                                const totalCell = document.createElement('td');
                                totalCell.className = 'align-start amount';
                                const total = document.createTextNode(sale.total);
                                totalCell.appendChild(total);
                                row.appendChild(totalCell);
                                const actionsCell = document.createElement('td');
                                actionsCell.className = 'align-middle white-space-nowrap text-end';
                                
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
                                detailLink.href = `/sale/detail/${sale.id}`;
                                detailLink.textContent = 'Detalle';
                                dropdownMenu.appendChild(detailLink);
                                if (sale.is_staff) {
                                    const editLink = document.createElement('a');
                                    editLink.className = 'dropdown-item';
                                    editLink.href = `/sale/update/${sale.id}`;
                                    editLink.textContent = 'Editar';
                                    dropdownMenu.appendChild(editLink);
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
                        // Ocultamos el loader despues de completar la busqueda
                        // loader.classList.add('d-none');
                    },
                    error: function (error) {
                        console.error('Error al realizar la búsqueda:', error);
                        searchResults.innerHTML = '<tr><td colspan="5">Error al realizar la búsqueda</td></tr>';

                        //Lo oculatamos tambien en caso de error
                        // loader.classList.add('d-none');
                    },
                });
            }

        }, 500) // Establecemos el retraso de 500 milisegundos
    });
});