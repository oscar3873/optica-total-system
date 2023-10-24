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
                    const selected_customer = document.getElementById('selected_customer'); // Aqui va el custoemr seleccionado
                    
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
            url: '/customers/new/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                console.log(data);
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
