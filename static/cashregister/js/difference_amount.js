
// Obtén una lista de todos los campos de monto manual
const countedAmountFields = Array.from(document.getElementsByClassName('difference-input'));

console.log(countedAmountFields);

// Función para calcular y actualizar la diferencia
function updateDifferences() {
    countedAmountFields.forEach((currentValue, index, array) => {

        const systemAmount = parseFloat(document.getElementById(`${index+1}`).textContent.replace('$', '').replace(',', ''));
        const countedAmount = parseFloat(currentValue.value === ''? 0: currentValue.value);
        const typeMethod = document.getElementById(`${index+1}`).dataset.typeMethod;
        const difference = isNaN(countedAmount) ? null : countedAmount - systemAmount;
        const differenceField = document.getElementById(`difference-${typeMethod}`);
        console.log(differenceField);
        if (difference === null) {
            differenceField.textContent = 'No válido';
        } else {
            const formatter = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
            });
            differenceField.textContent = formatter.format(difference);
        }
    });
}

// Agrega un evento de entrada a los campos de monto manual
countedAmountFields.forEach((field) => {
    field.addEventListener('input', updateDifferences);
});

// Calcula las diferencias iniciales
updateDifferences();
