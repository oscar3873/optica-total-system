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
                        item.dataset.customerCredit = customer.has_credit_account;
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
            const customerCredit = item.dataset.customerCredit;
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
            checkboxCustomer.id = `id_customer`;
            checkboxCustomer.hidden = true;
            checkboxCustomer.checked = true;
            const label = document.createElement("label");

            const titleH5Customer = document.createElement('h5');
            const textContentCustomer = document.createTextNode(customerName);
            titleH5Customer.appendChild(textContentCustomer);
            titleH5Customer.id = 'selecter_customer_title';
            label.classList.add('d-flex', 'align-items-center', 'mt-2'); // Agregar clases flex y alineación vertical al contenedor

            // Agregar el h5 al label primero
            label.appendChild(titleH5Customer);
            // Crear el botón
            var trash_delete = document.createElement("button");

            // Establecer atributos del botón
            trash_delete.setAttribute("class", "btn btn-falcon-default btn-sm ms-2"); // Agregar clase 'ms-2' para agregar margen a la izquierda
            trash_delete.setAttribute("type", "button");
            trash_delete.setAttribute("id", "button-delete-customer");
            trash_delete.setAttribute("title", "Eliminar Cliente");

            // Crear el ícono dentro del botón
            var icon = document.createElement("span");
            icon.setAttribute("class", "fas fa-trash text-danger");
            icon.setAttribute("data-fa-transform", "shrink-3 down-2");

            // Agregar el ícono al botón
            trash_delete.appendChild(icon);

            // Agregar el botón al label después del h5
            label.appendChild(trash_delete);

            checkboxContainer.appendChild(label);

            label.appendChild(checkboxCustomer);

            trash_delete.addEventListener("click", function(){
                payment_method.disabled = false;
                payment_method.options[selected_payment].selected = true;
                label.remove();
            });

            if (customerCredit == 1) {            
                // Recorre todas las opciones para encontrar la que contiene "Cuenta Corriente" en su texto
                for (var i = 0; i < payment_method.options.length; i++) {
                    if (payment_method.options[i].text.includes(searchText)) {
                        // Selecciona la opción encontrada
                        payment_method.options[i].selected = true;
                        
                        // Oculta el div con nombre 'boton-mas'
                        if (botonMasDiv) {
                            botonMasDiv.style.display = 'none';
                        }
                    }
                }
                payment_method.disabled = true;
            } else {
                // Activa la opción seleccionada
                payment_method.disabled = false;
                payment_method.options[selected_payment].selected = true;
            
                // Muestra el div con nombre 'boton-mas'
                if (botonMasDiv) {
                    botonMasDiv.style.display = 'block'; // O 'inline' según el tipo de display que uses
                }

            }


            

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

    // Obtén una referencia al botón "boton-realizar-venta" por su ID
    var realizarVentaBtn = document.getElementById('boton-realizar-venta');

    // Agrega un evento de clic al botón "boton-realizar-venta"
    realizarVentaBtn.addEventListener('click', function() {
        // Coloca aquí el código que deseas ejecutar al hacer clic en el botón "boton-realizar-venta"
        // En este caso, deshabilitar payment_method
        if (payment_method) {
            payment_method.disabled = false;
            for (var i = 0; i < payment_method.options.length; i++) {
                if (payment_method.options[i].text.includes(searchText)) {
                    // Selecciona la opción encontrada
                    payment_method.options[i].disabled = false;
                }
            }
        } else {
            console.error("payment_method no está definido o no es accesible desde este ámbito.");
        }
    });
});
