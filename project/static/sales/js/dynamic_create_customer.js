var button_serviceOrder = document.querySelector("[data-bs-target='#serviceOrder']");

let has_cristal = false;

let payment_method = document.getElementById('id_payment_method');
let selected_payment = 1;


document.addEventListener('DOMContentLoaded', function() {
    const saveCustomer = document.getElementById('save-customer');


    saveCustomer.addEventListener('click', function() {
        const formData = new FormData(document.getElementById('New-customer-form'));

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
                        const checkboxCustomer = document.createElement("input");
                        checkboxCustomer.type = "radio";
                        checkboxCustomer.classList.add('form-check-input', 'me-1', 'invisible');
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
                        label.classList.add('d-block', 'mt-2');

                        label.appendChild(titleH5Customer)
                        label.appendChild(checkboxCustomer);
                        checkboxContainer.appendChild(label);
                    }

                    if (customer_data.has_credit_account) {                
                        var searchText = "Cuenta Corriente";
                        // Recorre todas las opciones para encontrar la que contiene "Cuenta Corriente" en su texto
                        for (var i = 0; i < payment_method.options.length; i++) {
                            if (payment_method.options[i].text.includes(searchText)) {
                                // Selecciona la opción encontrada
                                payment_method.options[i].selected = true;
                            }
                        }
                    }else{
                        payment_method.options[selected_payment].selected = true;
                    }

                    // Cierra el modal al guardar exitosamente
                    $('#New-customer').modal('hide');

                    if (has_cristal){
                        button_serviceOrder.hidden = false;
                    }

                } else if ('error' in data) {
                    // Ha ocurrido un error al guardar el cliente
                    // let error_customer = document.getElementById('???');
                    // error_customer.textContent = data.error; 
                }
            }
        });
    });
});
