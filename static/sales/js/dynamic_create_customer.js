let payment_method = document.getElementById('id_form-0-payment_method');
let error_div = document.createElement('div');
let selected_payment = 0;

const customer_modal = document.getElementById('New-customer-form');
const searchText = "Cuenta Corriente";
const botonMasDiv = document.getElementById('boton-mas');
const amountInput = document.getElementById('id_form-0-amount');
const addPaymentContainer = document.getElementById('add-payment-container');


for (var i = 0; i < payment_method.options.length; i++) {
    if (payment_method.options[i].text.includes(searchText)) {
        // Selecciona la opción encontrada
        payment_method.options[i].disabled = true;
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const saveCustomer = document.getElementById('save-customer');

    saveCustomer.addEventListener('click', function() {
        const formData = new FormData(customer_modal);

        $.ajax({
            url: '/customers/new/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if ('customer' in data) {
                    const checkboxContainer = document.getElementById('selected_customer');
                    // Se ha guardado el cliente exitosamente
                    const customer_data = data.customer;

                    let selected_customer = document.getElementById('id_customer');
                    if (selected_customer){
                        let selecter_customer_title = document.getElementById('selecter_customer_title');
                        selecter_customer_title.textContent = `${customer_data.first_name} ${customer_data.last_name}`;

                        selected_customer.value = customer_data.id;
                    }else{
                        checkboxContainer.innerHTML = "";
                        const checkboxCustomer = document.createElement("input");
                        checkboxCustomer.type = "radio";
                        // Asegúrate de que todas las casillas de verificación tengan el mismo nombre
                        checkboxCustomer.name = "customer"; 
                        checkboxCustomer.value = customer_data.id;
                        checkboxCustomer.id = `id_customer`;
                        checkboxCustomer.hidden = true;
                        checkboxCustomer.checked = true;
                        
                        const label = document.createElement("label");
                        const titleH5Customer = document.createElement('h5')
                        const textContentCustomer = document.createTextNode(`${customer_data.first_name} ${customer_data.last_name}`);
                        titleH5Customer.appendChild(textContentCustomer);
                        titleH5Customer.id = 'selecter_customer_title';
                        label.classList.add('d-flex', 'align-items-center', 'mt-2'); // Agregar clases flex y alineación vertical al contenedor

                        label.appendChild(titleH5Customer)
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
                            amountInput.hidden = false;
                            addPaymentContainer.hidden = false;
                        });
                        label.appendChild(checkboxCustomer);
                        checkboxContainer.appendChild(label);
                    }

                    if (customer_data.has_credit_account) {    
                        // Recorre todas las opciones para encontrar la que contiene "Cuenta Corriente" en su texto
                        for (var i = 0; i < payment_method.options.length; i++) {
                            if (payment_method.options[i].text.includes(searchText)) {
                                // Selecciona la opción encontrada
                                payment_method.options[i].selected = true;
                                payment_method.disabled = true;
                                amountInput.hidden = true;
                                addPaymentContainer.hidden = true;
                                deleteNewPayments();
                                restoreAmount();
                                if (botonMasDiv) {
                                    botonMasDiv.style.display = 'none';
                                }
                            }
                        }
                    }else{
                        payment_method.options[selected_payment].selected = true;
                        payment_method.disabled = false;
                        amountInput.hidden = false;
                        addPaymentContainer.hidden = false;
                        // Muestra el div con nombre 'boton-mas'
                        if (botonMasDiv) {
                            botonMasDiv.style.display = 'block'; // O 'inline' según el tipo de display que uses
                        }
                    }

                    // Cierra el modal al guardar exitosamente
                    $('#New-customer').modal('hide');

                } else if ('error' in data) {
                    error_div.innerHTML = data.error;
                    error_div.className = "text-danger text-center";
                    
                    customer_modal.appendChild(error_div);
                }
            }
        });
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
    }
}

function restoreAmount(){
    const amountInput = document.getElementById('id_form-0-amount');
    amountInput.value = 0;
}