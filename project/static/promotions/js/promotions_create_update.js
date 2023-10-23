document.addEventListener("DOMContentLoaded", function () {
    const promotionInput = document.getElementById('id_type_discount');
    promotionInput.addEventListener('click', function () {
        const discountInput = document.getElementById('id_discount');
        if(promotionInput.value == 1){
            discountInput.setAttribute('disabled', 'true');
        }
        else{
            discountInput.removeAttribute("disabled");
        }
    })
    
});