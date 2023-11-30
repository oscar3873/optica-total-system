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
                        data.data.forEach(function (employee) {
                            const row = document.createElement('tr');
                            row.className = 'btn-reveal-trigger';

                            const firstNameCell = document.createElement('td');
                            firstNameCell.className = 'align-start first_name';

                            const avatarContainer = document.createElement('div');
                            avatarContainer.className = 'd-flex align-items-center';

                            const avatar = document.createElement('div');
                            avatar.className = 'avatar avatar-s me-1';

                            const avatarImage = document.createElement('img');
                            avatarImage.className = 'rounded-circle';
                            avatarImage.src = employee.image_url;
                            avatarImage.alt = '';
                            avatar.appendChild(avatarImage);
                            avatarContainer.appendChild(avatar);

                            const firstNameText = document.createTextNode(employee.first_name);
                            avatarContainer.textContent = employee.first_name;
                            firstNameCell.appendChild(avatarContainer);
                            row.appendChild(firstNameCell);

                            const lastNameCell = document.createElement('td');
                            lastNameCell.className = 'align-start last_name';
                            const lastNameText = document.createTextNode(employee.last_name);
                            lastNameCell.textContent = employee.last_name;
                            row.appendChild(lastNameCell);

                            const phoneNumberCell = document.createElement('td');
                            phoneNumberCell.className = 'align-start phone_number d-none d-sm-table-cell';
                            const phoneNumberLink = document.createElement('a');
                            phoneNumberLink.href = `https://wa.me/${employee.phone_code}${employee.phone_number}`;
                            phoneNumberLink.textContent = `${employee.phone_code}${employee.phone_number}`;
                            phoneNumberCell.appendChild(phoneNumberLink);
                            row.appendChild(phoneNumberCell);

                            const emailCell = document.createElement('td');
                            emailCell.className = 'align-start email d-none d-sm-table-cell';
                            const emailLink = document.createElement('a');
                            emailLink.href = `mailto:${employee.email}`;
                            emailLink.textContent = employee.email;
                            emailCell.appendChild(emailLink);
                            row.appendChild(emailCell);

                            const actionsCell = document.createElement('td');
                            actionsCell.className = 'align-middle white-space-nowrap text-start';
                            
                            const actionsButton = document.createElement('a');
                            actionsButton.href = `/employees/profile/${employee.id}`;
                            actionsButton.className = 'btn btn-sm btn-falcon-default';
                            actionsButton.setAttribute('data-bs-toggle', 'tooltip');
                            actionsButton.setAttribute('title', 'Ver Detalle');
                            const actionsIcon = document.createElement('span');
                            actionsIcon.className = 'fas fa-eye';
                            actionsButton.appendChild(actionsIcon);

                            const dropdownMenu = document.createElement('div');
                            dropdownMenu.className = 'dropstart font-sans-serif position-static d-inline-block';
                            
                            let actionsDropdown = document.createElement('div');
                            actionsDropdown.className = 'd-flex gap-2 py-0'; 
                            actionsDropdown.appendChild(actionsButton);

                            if (employee.is_staff) {
                                const editLink = document.createElement('a');
                                editLink.href = `/employees/update/${employee.id}`;
                                editLink.className = 'btn btn-sm btn-falcon-default';
                                editLink.setAttribute('data-bs-toggle', 'tooltip');
                                editLink.setAttribute('title', 'Editar');
                                const editIcon = document.createElement('span');
                                editIcon.className = 'fas fa-edit';
                                editLink.appendChild(editIcon);
                            
                                const deleteLink = document.createElement('a');
                                deleteLink.href = `/employees/delete/${employee.id}/`;
                                deleteLink.className = 'btn btn-sm btn-falcon-default';
                                const deleteIcon = document.createElement('span');
                                deleteIcon.className = 'fas fa-trash text-danger';
                                deleteLink.appendChild(deleteIcon);                                
                                
                                actionsDropdown.appendChild(editLink);
                                actionsDropdown.appendChild(deleteLink);
                            }

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