document.addEventListener('DOMContentLoaded', function() {
    const labelTotalAmount = document.getElementById('total-amount-payments');
    const btnPay = document.getElementById('btn-pagar');
    btnPay.addEventListener('click', function() {
        let totalAmpunt = sumPayments();
        labelTotalAmount.innerHTML = `$ ${totalAmpunt}`;
    });

});

function sumPayments(){
    let sum = 0;
    const inputsContainer = document.getElementById('payment-methods-container');
    const elements = inputsContainer.querySelectorAll('[id^="id_form-"]');
    let arrayElements = Array.from(elements);
    for (let i = 1; i < elements.length; i=i+2) {
        sum += parseInt(arrayElements[i].value);
    }
    return sum;
}
