let idCustomerGlobal;
document.addEventListener("DOMContentLoaded", function () {
    
    function configureSearch(searchInput, searchResults, fieldIdentifier) {
        searchInput.addEventListener('input', (event) => {
            const searchTerm = event.target.value.trim().toLowerCase();
            if (!searchTerm) {
                // Limpiar los resultados de búsqueda si no hay término de búsqueda
                searchResults.innerHTML = '';
                return;
            }

            // Realizar la búsqueda de clientes que coincidan con el término de búsqueda
            $.ajax({
                url: `/customers/ajax-search-customers/?search_term=${searchTerm}`,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    const customers = data.data;
                    // Mostrar los resultados de búsqueda
                    searchResults.innerHTML = ''; // Limpia los resultados anteriores
                    customers.forEach(customer => {
                        const item = document.createElement('li');
                        item.style.zIndex = "3";
                        item.style.backgroundColor = '#464c55';
                        item.style.cursor = 'pointer';
                        item.classList.add('list-group-item', 'customers');
                        item.dataset.customerId = customer.id;
                        item.innerHTML = `
                        <div class="d-flex justify-content-between">
                            <h6>${customer.first_name} ${customer.last_name}</h6>
                            <small>${customer.dni}</small>
                        </div>
                        `;
                        searchResults.appendChild(item);
                    });
                },
                error: function(error) {
                    console.error('Error en la solicitud AJAX', error);
                }
            });
        });

        searchResults.addEventListener('click', (event) => {
            const checkboxContainer = document.getElementById('selected_customer');
            //Si tiene hijo hay que eliminarlos para que ponga los nuevos
            if(checkboxContainer.hasChildNodes()){
                while(checkboxContainer.firstChild){
                    checkboxContainer.removeChild(checkboxContainer.firstChild);
                }
            }

            const item = event.target.closest('.customers');
            if (!item) {
                return;
            }

            const customerId = item.dataset.customerId;
            idCustomerGlobal=customerId;
            const customerName = item.querySelector('h6').textContent;

            // Rellenar el campo del customer seleccionado y ocultar los resultados de búsqueda
            searchInput.value = '';
            searchResults.innerHTML = '';

            const checkboxCustomer = document.createElement("input");
            checkboxCustomer.type = "radio";
            checkboxCustomer.classList.add('form-check-input', 'me-1', 'invisible');
            // Asegúrate de que todas las casillas de verificación tengan el mismo nombre
            checkboxCustomer.name = "customer"; 
            checkboxCustomer.value = customerId;
            checkboxCustomer.id = `${customerName}`;
            checkboxCustomer.checked = true;
            const label = document.createElement("label");
            const titleH5Customer = document.createElement('h5')
            const textContentCustomer = document.createTextNode(customerName);
            titleH5Customer.appendChild(textContentCustomer);
            label.classList.add('d-block', 'mt-2');

            label.appendChild(titleH5Customer)
            label.appendChild(checkboxCustomer);
            checkboxContainer.appendChild(label);
            // Añadir el ID del customer al formulario
            const customerIdCheck = document.createElement('input');
            customerIdCheck.type = 'hidden';
            customerIdCheck.name = `selected_customer_id_${fieldIdentifier}`;
            customerIdCheck.value = customerId;
            searchInput.closest('form').appendChild(customerIdCheck);
        });
    }

    function configureSearchInputs(form, count) {
        const fieldPrefix = `id_form-${count}`;
        const searchInputA = form.querySelector(`#${fieldPrefix}-search-customerA-input`);
        const searchResultsA = form.querySelector(`#${fieldPrefix}-search-customerA-results`);
        configureSearch(searchInputA, searchResultsA, 'customerA');
    }

    // SOLO PARA EL FORMULARIO 1
    const form_0 = document.getElementById('id_form-0');
    configureSearchInputs(form_0, 0);
});
