let payment_method = document.getElementById('id_payment_method');
let error_div = document.createElement('div');
let selected_payment = 1;
const customer_modal = document.getElementById('New-customer-form');
const searchText = "Cuenta Corriente";

for (var i = 0; i < payment_method.options.length; i++) {
    if (payment_method.options[i].text.includes(searchText)) {
        // Selecciona la opción encontrada
        payment_method.options[i].disabled = true;
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const saveCustomer = document.getElementById('save-customer');
    const botonMasDiv = document.getElementById('boton-mas');


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
                        // Recorre todas las opciones para encontrar la que contiene "Cuenta Corriente" en su texto
                        for (var i = 0; i < payment_method.options.length; i++) {
                            if (payment_method.options[i].text.includes(searchText)) {
                                // Selecciona la opción encontrada
                                payment_method.options[i].selected = true;
                                payment_method.disabled = true;
                                if (botonMasDiv) {
                                    botonMasDiv.style.display = 'none';
                                }
                            }
                        }
                    }else{
                        payment_method.options[selected_payment].selected = true;
                        payment_method.disabled = false;
                        // Muestra el div con nombre 'boton-mas'
                        if (botonMasDiv) {
                            botonMasDiv.style.display = 'block'; // O 'inline' según el tipo de display que uses
                        }
                    }

                    // Cierra el modal al guardar exitosamente
                    $('#New-customer').modal('hide');

                } else if ('error' in data) {
                    console.log(data.error);
                    error_div.innerHTML = data.error;
                    error_div.className = "text-danger text-center";
                    
                    customer_modal.appendChild(error_div);
                }
            }
        });
    });
});
