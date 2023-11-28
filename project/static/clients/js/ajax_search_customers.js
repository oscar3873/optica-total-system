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
                        data.data.forEach(function (customer) {
                            const row = document.createElement('tr');
                            row.className = 'btn-reveal-trigger';

                            const firstNameCell = document.createElement('td');
                            firstNameCell.className = 'align-start first_name';
                            const firstNameText = document.createTextNode(customer.first_name);
                            firstNameCell.appendChild(firstNameText);
                            row.appendChild(firstNameCell);

                            const lastNameCell = document.createElement('td');
                            lastNameCell.className = 'align-start last_name';
                            const lastNameText = document.createTextNode(customer.last_name);
                            lastNameCell.appendChild(lastNameText);
                            row.appendChild(lastNameCell);

                            const phoneNumberCell = document.createElement('td');
                            phoneNumberCell.className = 'align-start phone_number d-none d-md-table-cell';
                            const phoneNumberLink = document.createElement('a');
                            phoneNumberLink.href = `https://wa.me/${customer.phone_code}${customer.phone_number}`;
                            phoneNumberLink.textContent = `${customer.phone_code}${customer.phone_number}`;
                            phoneNumberCell.appendChild(phoneNumberLink);
                            row.appendChild(phoneNumberCell);

                            const dniCell = document.createElement('td');
                            dniCell.className = 'align-start dni d-none d-md-table-cell';
                            const dniText = document.createTextNode(customer.dni);
                            dniCell.appendChild(dniText);
                            row.appendChild(dniCell);

                            const userMadeCell = document.createElement('td');
                            userMadeCell.className = 'align-start user_made d-none d-md-table-cell';
                            const userMadeText = document.createTextNode(customer.user_made);
                            userMadeCell.appendChild(userMadeText);
                            row.appendChild(userMadeCell);

                            const creditAccountCell = document.createElement('td');
                            creditAccountCell.className = 'align-start dni d-none d-md-table-cell';

                            const creditAccountText = document.createElement("span");
                                creditAccountText.className = 'badge rounded-pill badge-soft-secondary';
                                creditAccountText.textContent = "Sin cuenta"; 

                            if (customer.has_credit_account) {
                                creditAccountText.className = 'badge rounded-pill badge-soft-success';
                                creditAccountText.textContent = "Cuenta abierta"; 
                            }
                            creditAccountCell.appendChild(creditAccountText);
                            row.appendChild(creditAccountCell);

                            const actionsCell = document.createElement('td');
                            actionsCell.className = 'align-middle white-space-nowrap text-start';
                            
                            const actionsDropdown = document.createElement('div');
                            actionsDropdown.className = 'dropstart font-sans-serif position-static d-inline-block';

                            const actionsButton = document.createElement('a');
                            actionsButton.href = `/customers/detail/${customer.id}`;
                            actionsButton.className = 'btn btn-sm btn-falcon-default me-2';
                            actionsButton.setAttribute('data-bs-toggle', 'tooltip');
                            actionsButton.setAttribute('title', 'Ver Detalle');
                            const actionsIcon = document.createElement('span');
                            actionsIcon.className = 'fas fa-eye';
                            actionsButton.appendChild(actionsIcon);

                            const dropdownMenu = document.createElement('div');
                            dropdownMenu.className = 'dropstart font-sans-serif position-static d-inline-block';

                            // const detailLink = document.createElement('a');
                            // detailLink.className = 'dropdown-item';
                            // detailLink.href = `/customers/detail/${customer.id}`;
                            // detailLink.textContent = 'Detalle';
                            // dropdownMenu.appendChild(detailLink);
                            if (customer.is_staff) {
                                const editLink = document.createElement('a');
                                editLink.href = `/customers/update/${customer.id}`;
                                editLink.className = 'btn btn-sm btn-falcon-default me-2';
                                editLink.setAttribute('data-bs-toggle', 'tooltip');
                                editLink.setAttribute('title', 'Editar');
                                const editIcon = document.createElement('span');
                                editIcon.className = 'fas fa-edit';
                                editLink.appendChild(editIcon);
                            
                                const deleteLink = document.createElement('a');
                                deleteLink.href = `/customers/delete/${customer.id}/`;
                                deleteLink.className = 'btn btn-sm btn-falcon-default';
                                const deleteIcon = document.createElement('span');
                                deleteIcon.className = 'fas fa-trash text-danger';
                                deleteLink.appendChild(deleteIcon);                                dropdownMenu.appendChild(editLink);
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