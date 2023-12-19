
// Lista de todos los campos de monto manual
const countedAmountFields = Array.from(document.getElementsByClassName('difference-input'));


function parseFormattedNumber(numberString) {
    // Reemplaza el separador de miles y luego el separador decimal para obtener un formato flotante
    return parseFloat(numberString.replace(/\./g, '').replace(/,/, '.'));
}

function formatNumberAsCurrency(number) {
    // Formatea el número como decimal sin símbolo de moneda
    const formatter = new Intl.NumberFormat('es', {
        style: 'decimal',
        minimumFractionDigits: 2, // Para mantener dos decimales
    });
    return formatter.format(number);
}

// Función para calcular y actualizar la diferencia
function updateDifferences() {
    countedAmountFields.forEach((currentValue, index) => {
        const systemAmountString = document.getElementById(`${index+1}`).textContent.replace('$', '').trim();
        const systemAmount = parseFormattedNumber(systemAmountString);
        const countedAmount = parseFormattedNumber(currentValue.value === '' ? '0' : currentValue.value);
        const typeMethod = document.getElementById(`${index+1}`).dataset.typeMethod;
        const difference = isNaN(countedAmount) ? null : countedAmount - systemAmount;
        const differenceField = document.getElementById(`difference-${typeMethod}`);

        if (difference === null) {
            differenceField.textContent = 'No válido';
        } else {
            differenceField.textContent = formatNumberAsCurrency(difference);
        }
    });
}

// Agrega un evento de entrada a los campos de monto manual
countedAmountFields.forEach((field) => {
    field.addEventListener('input', updateDifferences);
});

// Calcula las diferencias iniciales
updateDifferences();
