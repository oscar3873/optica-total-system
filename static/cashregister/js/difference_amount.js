
// Lista de todos los campos de monto manual
const countedAmountFields = Array.from(document.getElementsByClassName('difference-input'));


function parseFormattedNumber(numberString) {
    // Reemplaza el separador de miles y luego el separador decimal para obtener un formato flotante
    return parseFloat(numberString.replace(/\./g, '').replace(/,/, '.'));
}

function parseInputNumber(inputString) {
    // Esta función se usa para manejar los valores ingresados en los campos de entrada
    return parseFloat(inputString.replace(/,/, '.'));
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
        console.log("Este el total del sistema: " + systemAmountString);
        const systemAmount = parseFormattedNumber(systemAmountString);
        
        // Utiliza la función parseInputNumber para los valores de entrada
        const countedAmount = parseInputNumber(currentValue.value === '' ? '0' : currentValue.value);
        console.log("Este es el valor del campo: " + countedAmount);
        
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
