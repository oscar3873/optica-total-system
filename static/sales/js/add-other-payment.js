document.addEventListener("DOMContentLoaded", function() {
    const btnAddInputs = document.getElementById('addPayment');
    const inputsContainer = document.getElementById('payment-methods-container');
  
    
    btnAddInputs.addEventListener( "click", function() {
        const inputCount = document.getElementById('id_form-TOTAL_FORMS');
        count = inputCount.value;

        // Obtén el elemento select por su ID (reemplaza 'id_form-0-payment_method' con el ID real de tu select)
        const paymentMethodInput = document.getElementById('id_form-0-payment_method');
        // Selecciona todos los elementos option dentro del select
        const optionsOfSelect = paymentMethodInput.querySelectorAll('option');
        let options = [];
        // Recorro todas las opciones del select
        optionsOfSelect.forEach(function(option) {
            if(option.text != 'Cuenta Corriente - Cuenta Corriente'){
                options.push({
                    value: option.value,
                    label: option.text.trim() // Trim elimina espacios en blanco al principio y al final del texto
                });
            }
        });


        //Creación del select
        const selectPaymentElement = document.createElement('select');
        selectPaymentElement.name = `form-${count}-payment_method`;
        selectPaymentElement.className = 'form-control';
        selectPaymentElement.id = `id_form-${count}-payment_method`;
        
        // Agrego las opciones al select
        options.forEach(function(option) {
            let optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.label;
            selectPaymentElement.appendChild(optionElement);
        });

        // Creación del div contenedor del select
        let divSelect = document.createElement('div');
        divSelect.classList.add('col-6');
        // Agrego el select al contenedor
        divSelect.appendChild(selectPaymentElement);



        // Creación el elemento input de tipo número para ingresar el monto
        var inputElement = document.createElement('input');
        inputElement.type = 'number';
        inputElement.name = `form-${count}-amount`;
        inputElement.value = '0';
        inputElement.className = 'form-control';
        inputElement.step = 'any';
        inputElement.id = `id_form-${count}-amount`;


        // Creación del div contenedor input de monto
        const divInput= document.createElement('div');
        divInput.classList.add('col-8');
        // Agrego el input al contenedor
        divInput.appendChild(inputElement);


        // Creación del btn de eliminar
        const btnElement = document.createElement('button');
        btnElement.type = 'button';
        btnElement.id = `delete-payment-${count}`
        btnElement.title = 'Eliminar pago';
        btnElement.classList.add('btn','btn-falcon-default','btn-sm','mt-1');
        btnElement.innerHTML = `<span class="fas fa-trash text-danger" data-fa-transform="shrink-3 down-2"></span>`

        


        // Creación del div contenedor del btn
        const divBtn= document.createElement('div');
        divBtn.classList.add('col-4');
        // Agrego el btn al contenedor del btn
        divBtn.appendChild(btnElement);

        
        // Creación del div contenedor input de monto y el btn de eliminarción
        const divInputAndBtn= document.createElement('div');
        divInputAndBtn.classList.add('row');
        divInputAndBtn.appendChild(divInput);
        divInputAndBtn.appendChild(divBtn);

        // Creacón del segundo div col-6
        const divInputAndBtnContainer = document.createElement('div');
        divInputAndBtnContainer.classList.add('col-6');
        divInputAndBtnContainer.appendChild(divInputAndBtn);



        //Creación del div contedor de los 2 divs
        const divContainerElement = document.createElement('div');
        divContainerElement.classList.add('row','p-0','m-0','pt-3');
        // Agrego los 2 divs contenedores
        divContainerElement.appendChild(divSelect);
        divContainerElement.appendChild(divInputAndBtnContainer);


        //Agrego el div contenedor al contenedor del template
        inputsContainer.appendChild(divContainerElement);

        btnElement.addEventListener('click', function(){
            // Remover el div contenedor de los elemtentos
            divContainerElement.remove();
            // Dismiuir el count del form
            modifyCountForm(false);
            // Renumerar id y name de los elementos siguientes
            updateIdAndName();
        });
        
        //Incrementar el contador del form
        modifyCountForm(true);

    });


});



function updateIdAndName(){
    const inputsContainer = document.getElementById('payment-methods-container');
    const elements = inputsContainer.querySelectorAll('[id^="id_form-"]');
    let count = 0;
    arrayElements = Array.from(elements);
    for (let i = 0; i < elements.length; i=i+2) {
        if(arrayElements[i].id != `id_form-${count}-payment_method`){
            elements[i].id = `id_form-${count}-payment_method`;
            elements[i].name = `form-${count}-payment_method`;
            elements[i+1].id = `id_form-${count}-amount`;
            elements[i+1].name = `form-${count}-amount`;
        }
    count++;
    }
}


function modifyFirstNumOfStr(text,increase) {
    let num = extractNumbersFromText(text)[0];
    if(increase){
        return text.replace(num,num+1);
    }
    else{
        return text.replace(num,num-1);
    }
}

// Extrae numeros de un string, devuelve un array de str con los numeros.
// Ej: carlos01A23 => ['01','23']
function extractNumbersFromText(text) {
    return  text.match(/\d+/g);
}


// Incrementa (o disminuye) el contador del input que tiene la cantidad de forms
function modifyCountForm(increase){
    const inputCount = document.getElementById('id_form-TOTAL_FORMS');
    if(increase){
        inputCount.value = parseInt(inputCount.value) + 1;
    }
    else{
        inputCount.value = parseInt(inputCount.value) - 1;
    }
}