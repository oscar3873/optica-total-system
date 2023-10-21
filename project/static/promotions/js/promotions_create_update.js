document.addEventListener("DOMContentLoaded", function () {
    const promotionInput = document.getElementById('id_form-0-type_discount');
    promotionInput.addEventListener('click', function () {
        // CAMBIAR AQUI POR EL ID DEL BTN DEL INPUT DE DESCUENTO
        const discountInput = document.getElementById('id_form-0-start_date');
        if(promotionInput.value == 'A'){
            discountInput.setAttribute('disabled', 'true');
        }
        else{
            discountInput.removeAttribute("disabled");
        }
    })
    
});