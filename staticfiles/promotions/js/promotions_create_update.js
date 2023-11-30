document.addEventListener("DOMContentLoaded", function () {
    const promotionInput = document.getElementById('id_type_discount');
    const discountInput = document.getElementById('id_discount');
    let optionIndex = promotionInput.selectedIndex;

    if(promotionInput.options[optionIndex].text.includes('2x1')){
        discountInput.setAttribute('disabled', 'true');
    }
    promotionInput.addEventListener('click', function () {
        optionIndex = promotionInput.selectedIndex
        if(promotionInput.options[optionIndex].text.includes('2x1')){
            discountInput.setAttribute('disabled', 'true');
            discountInput.value = '0';
        }
        else{
            discountInput.removeAttribute("disabled");
        }
    });

    const productsSelectedContainer = document.getElementById('products-selected');
    if(productsSelectedContainer.classList.contains('update')){
        const checkboxes = Array.from(productsSelectedContainer.querySelectorAll('input[type="checkbox"]'));
        checkboxes.forEach(cheeckbox => {
            cheeckbox.classList.add('form-check-input');
        });
    }   
});