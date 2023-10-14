document.addEventListener('DOMContentLoaded', function() {
    const saveCustomer = document.getElementById('save-customer');
    const inputSearchCustomer = document.getElementById('search-customer');	

    inputSearchCustomer.addEventListener('input', function(){

        $.ajax({
            url: '/customers/ajax-search-customers/',
            type: 'GET',
            processData: false,
            contentType: false,
            success: function(data) {
                if (data) {
                    const customers_select = document.getElementById('customer-container');

                    if (inputSearchCustomer.value === ''){
                        //Eliminar todos los childrens del DOM
                        customers_select.children = '';
                    }
                    // Se ha guardado el cliente exitosamente
                    const customer_list = data.data;
        
                    // Obtén las opciones existentes en el select
                    const existingOptions = new Set([...customers_select.children].map(option => parseInt(option.value, 10)));
                    console.log(existingOptions);
                    customer_list.forEach(customer_data => {
                        // Comprueba si el valor ya existe en las opciones existentes
                        if (!existingOptions.has(parseInt(customer_data.id, 10))) {
                            const rowCustomer = document.createElement('option');
                            rowCustomer.value = customer_data.id;
                            rowCustomer.text = customer_data.last_name + ', ' + customer_data.first_name;
                            
                            customers_select.appendChild(rowCustomer);
        
                            // Agrega el nuevo valor al conjunto de opciones existentes
                            existingOptions.add(customer_data.id);
                        }
                    });
        
                    // Cierra el modal al guardar exitosamente
                    $('#New-customer').modal('hide');
                } else {
                    // Ha ocurrido un error al guardar el cliente
                    console.error(data.error);
                }
            }
        });
    });

    saveCustomer.addEventListener('click', function() {
        const formData = new FormData(document.getElementById('New-customer-form'));

        $.ajax({
            url: '/customers/ajax-new-customers/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if ('customer' in data) {
                    const customers_list = document.getElementById('customer-container');
                    // Se ha guardado el cliente exitosamente
                    const customer_data = data.customer;

                    const rowCustomer = document.createElement('div');
                    rowCustomer.classList.add('d-block');
                    const customer = document.createElement('div');
                    customer.textContent = customer_data.first_name + ', ' + customer_data.first_name;

                    rowCustomer.appendChild(customer);
                    customers_list.appendChild(rowCustomer);
                    
                    // Cierra el modal al guardar exitosamente
                    $('#New-customer').modal('hide');
                } else if ('error' in data) {
                    // Ha ocurrido un error al guardar el cliente
                    console.error(data.error);
                }
            }
        });
    });
});
