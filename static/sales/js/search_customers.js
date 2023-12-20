let idCustomerGlobal;

document.addEventListener("DOMContentLoaded", function () {
    const amountInput = document.getElementById('id_form-0-amount');
    const addPaymentContainer = document.getElementById('add-payment-container');
    
    function configureSearch(searchInput, searchResults, fieldIdentifier) {
        searchInput.addEventListener('input', (event) => {
            let searchTerm = event.target.value.trim().toLowerCase();
            if (!searchTerm) {
                // Limpiar los resultados de búsqueda si no hay término de búsqueda
                searchResults.innerHTML = '';
                return;
            }

            // Realizar la búsqueda de clientes que coincidan con el término de búsqueda
            $.ajax({
                url: `/customers/ajax-search-customers/`,
                data: { search_term: searchTerm },
                success: function(data) {
                    let customers = data.data;
                
                    // Mostrar los resultados de búsqueda
                    searchResults.innerHTML = ''; // Limpia los resultados anteriores
                    // Define el límite de resultados a mostrar (5 en este caso)
                    const limit = 5;
                
                    for (let index = 0; index < customers.length && index < limit; index++) {
                        let customer = customers[index];
                        const item = document.createElement('li');
                        item.style.zIndex = "3";
                        item.style.cursor = 'pointer';
                        item.classList.add('list-group-item', 'searchType', 'list-group-item-secondary', 'customers');
                        item.dataset.customerId = customer.id;
                        item.dataset.customerCredit = customer.has_credit_account;
                        item.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <h6>${customer.first_name} ${customer.last_name}</h6>
                                <small>${customer.dni}</small>
                            </div>
                        `;
                        searchResults.appendChild(item);
                    }
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
                amountInput.hidden = false;
                addPaymentContainer.hidden = false;
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
                amountInput.hidden = true;
                addPaymentContainer.hidden = true;
                deleteNewPayments();
                restoreAmount();
            } else {
                // Activa la opción seleccionada
                payment_method.disabled = false;
                payment_method.options[selected_payment].selected = true;
                amountInput.hidden = false;
                addPaymentContainer.hidden = false;
            
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
        // Espera 500 milisegundos (0.5 segundos) antes de cambiar el tipo del botón
        setTimeout(() => {
            realizarVentaBtn.type = "button";
        }, 1); // Ajusta el tiempo de espera según tus necesidades
        // Coloca aquí el código que deseas ejecutar al hacer clic en el botón "boton-realizar-venta"
        // En este caso, deshabilitar payment_method
        let customer_selected = document.getElementById('id_customer');
        let amount_input = document.getElementById('id_amount');
        let commision_user = document.getElementById('id_commision_user');

        if (payment_method && customer_selected && amount_input.value != '' && commision_user.value != '') {
            payment_method.disabled = false;
            for (var i = 0; i < payment_method.options.length; i++) {
                if (payment_method.options[i].text.includes(searchText)) {
                    // Selecciona la opción encontrada
                    payment_method.options[i].disabled = false;
                }
            }
            amountInput.hidden = false;
            addPaymentContainer.hidden = false;
        } else {
            console.error("payment_method no está definido o no es accesible desde este ámbito.");
        }
    });
});

function deleteNewPayments(){
    const methodsPaymentContainer = document.getElementById('payment-methods-container');
    const listNewPayments = methodsPaymentContainer.getElementsByClassName('new-payment');
    let ArrayNewPayments = Array.from(listNewPayments);
    if (ArrayNewPayments.length > 0) {
        ArrayNewPayments.forEach(function(child) {
            child.parentNode.removeChild(child);
        });
        const countForms = document.getElementById('id_form-TOTAL_FORMS');
        countForms.value = 1;
    }
}

function restoreAmount(){
    const amountInput = document.getElementById('id_form-0-amount');
    amountInput.value = 0;
}