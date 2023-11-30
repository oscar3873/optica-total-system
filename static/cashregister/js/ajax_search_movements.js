document.addEventListener('DOMContentLoaded', () => {
    //Para poder ponerle un pequeño delay
    let timeoutId;

    //loader para los movimientos
    // const loader = document.getElementById('loader-movements');

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
                            data.data.forEach(function (movement) {
                                const row = document.createElement('tr');
                                row.className = 'btn-reveal-trigger';
    
                                const nameCell = document.createElement('td');
                                nameCell.className = 'align-start user_made d-none d-sm-table-cell px-4';
                                const nameText = document.createTextNode(movement.user_made);
                                nameCell.appendChild(nameText);
                                row.appendChild(nameCell);
    
                                const amountCell = document.createElement('td');
                                amountCell.className = 'align-start amount px-4';
                                const barcodeText = document.createTextNode(movement.amount);
                                amountCell.appendChild(barcodeText);
                                row.appendChild(amountCell);
    
                                const dateMovementCell = document.createElement('td');
                                dateMovementCell.className = 'align-start date_movement px-4 d-none d-sm-table-cell';
                                const descriptionText = document.createTextNode(movement.date_movement);
                                dateMovementCell.appendChild(descriptionText);
                                row.appendChild(dateMovementCell);
    
                                const typeOperationCell = document.createElement('td');
                                typeOperationCell.className = 'align-start type_operation px-4';
                                const typeOperationSpan = document.createElement('span');
                                typeOperationSpan.className = movement.type_operation === 'Ingreso'?'badge rounded-pill badge-soft-success': 'badge rounded-pill badge-soft-danger';
                                const typeOperationText = document.createTextNode(`${movement.type_operation}`);
                                typeOperationSpan.appendChild(typeOperationText);
                                typeOperationCell.appendChild(typeOperationSpan);
                                row.appendChild(typeOperationCell);
    
                                const actionsCell = document.createElement('td');
                                actionsCell.className = 'align-middle white-space-nowrap text-start';
                                
                                const actionsDropdown = document.createElement('div');
                                actionsDropdown.className = 'dropstart font-sans-serif position-static d-inline-block';

                                const actionsButton = document.createElement('a');
                                actionsButton.href = `/movements/detail/${movement.id}`;
                                actionsButton.className = 'btn btn-sm btn-falcon-default me-2';
                                actionsButton.setAttribute('data-bs-toggle', 'tooltip');
                                actionsButton.setAttribute('title', 'Ver Detalle');
                                const actionsIcon = document.createElement('span');
                                actionsIcon.className = 'fas fa-eye';
                                actionsButton.appendChild(actionsIcon);

                                const dropdownMenu = document.createElement('div');
                                dropdownMenu.className = 'dropstart font-sans-serif position-static d-inline-block';

                                actionsDropdown.appendChild(actionsButton);

                                if (movement.is_staff) {
                                    const editLink = document.createElement('a');
                                    editLink.href = `/movements/update/${movement.id}`;
                                    editLink.className = 'btn btn-sm btn-falcon-default me-2';
                                    editLink.setAttribute('data-bs-toggle', 'tooltip');
                                    editLink.setAttribute('title', 'Editar');
                                    const editIcon = document.createElement('span');
                                    editIcon.className = 'fas fa-edit';
                                    editLink.appendChild(editIcon);
                                
                                    // const deleteLink = document.createElement('a');
                                    // deleteLink.href = `/movements/delete/${customer.id}/`;
                                    // deleteLink.className = 'btn btn-sm btn-falcon-default';
                                    // const deleteIcon = document.createElement('span');
                                    // deleteIcon.className = 'fas fa-trash text-danger';
                                    // deleteLink.appendChild(deleteIcon);
                                    // dropdownMenu.appendChild(deleteLink);
                                    actionsDropdown.appendChild(editLink);
                                }

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

        }, 0) // Establecemos el retraso de 500 milisegundos
    });
});