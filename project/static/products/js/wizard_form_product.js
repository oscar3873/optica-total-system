document.addEventListener('DOMContentLoaded', function() {
    
    let typesContainer = document.getElementById('types-container');
    typesContainer.classList.add('row');
    let checkboxes = document.getElementsByName("features");
    var typeSet = new Set();
    checkboxes.forEach(function(checkbox) {
        var textSeparated = checkbox.parentElement.textContent.trim().split(" - ");
        typeSet.add(textSeparated[0]);
    });

    
    // Variable para rastrear si el modal está abierto
    let isModalOpen = false;

    for (let type of typeSet) {
        // Contenedor del tipo
        let typeContainer = document.createElement('div');
        typeContainer.classList.add('col-12','col-sm-6', 'col-md-3', 'pt-2');

        let typeTitle = document.createElement('label');
        typeTitle.classList.add('mb-0','fw-bold');
        typeTitle.textContent = `${type}`;

        // Contenedor que alinea horizontalmente el label y el botón
        let textButtonContainer_unit = document.createElement('div');
        textButtonContainer_unit.classList.add('d-flex', 'align-items-center');

        // Contenedor de los checkboxes
        let checkboxContainer_unit = document.createElement('div');
        checkboxContainer_unit.classList.add('col-md-12', 'mx-4', 'pt-1');
        checkboxContainer_unit.id = `${type}`;

        textButtonContainer_unit.appendChild(typeTitle);

        typeContainer.appendChild(textButtonContainer_unit);


        // Creacion del btn para agregar más caracteristicas (valores)
        let btnAdd = document.createElement('span');
        btnAdd.setAttribute('title','Agregar uno nuevo');
        btnAdd.classList.add('fa-stack','ms-1','ms-sm-0');
        btnAdd.style.fontSize = '.6em';
        btnAdd.style.cursor = 'pointer';
        btnAdd.innerHTML = `<i class="fas fa-circle fa-stack-2x text-primary"></i>
        <i class="fa-inverse fa-stack-1x dark__text-white fas fa-plus"></i>`;
        
        btnAdd.addEventListener('click', function() {
            if (!isModalOpen) {
                // Actualiza el título del modal con el tipo correspondiente
                let modal = $('#Feature-unit-modal');
                // modal.find('.modal-title').text('Añade un nuevo valor para ' + type);
                modal.find('.modal-title').text('Agregar uno nuevo a ' + type);

                modal.modal('show');

                // Obtén el campo de entrada con ID "id_type" dentro del formulario
                let inputField = modal.find('#Feature-unit-form #id_type');

                inputField.attr('type', 'hidden');
                inputField.val(type);

                isModalOpen = true;

                modal.on('hidden.bs.modal', function() {
                    isModalOpen = false;
                });
            }
        });

        // Agrega el botón "+" al título del Tipo de Característica
        textButtonContainer_unit.appendChild(btnAdd);

        for (let checkbox of checkboxes) {
            let labelElement = checkbox.parentElement;
            let textLabel = labelElement.textContent.trim();
            let textSeparated = textLabel.split(" - ");
            let textType = textSeparated[0];
            if (textType == type) {
                let labelClone = labelElement.cloneNode(true);
                let inputClone = labelClone.firstElementChild;
                labelClone.textContent = textSeparated[1];
                labelClone.appendChild(inputClone);
                labelClone.classList.add('d-block');
                checkboxContainer_unit.appendChild(labelClone);
            }
        }

        typeContainer.appendChild(textButtonContainer_unit);
        typeContainer.appendChild(checkboxContainer_unit);
        typesContainer.appendChild(typeContainer);
    }
    const featuresContainer = document.getElementById('feature_checks');
    featuresContainer.remove();

    $('#save-feature-unit').on('click', function() {
        var checkboxes = document.querySelectorAll('input[type="checkbox"][id^="id_features_"]');
        var uniqueCheckboxIDs = new Set();
        
        checkboxes.forEach(function(checkbox) {
            uniqueCheckboxIDs.add(checkbox.id);
        });
        
        var cantidad_unit = uniqueCheckboxIDs.size;
        // Obtener el formulario dentro del modal
        let modalForm = $('#Feature-unit-form');
    
        // Obtener los datos del formulario
        let formData = new FormData(modalForm[0]);
    
        // Realizar la solicitud AJAX
        $.ajax({
            url: '/products/new/feature_unit/',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.status === 'success') {
                    // Obtén el tipo correspondiente
                    let type = data.new_feature_unit.type; // Asegúrate de tener este valor en los datos de la respuesta AJAX
    
                    // Encuentra el contenedor de checkboxes adecuado usando el identificador único
                    let checkboxContainer_unit = document.getElementById(type);
    
                    let new_check_unit = document.createElement('input');
                    let new_label_unit = document.createElement('label');

                    new_check_unit.type = 'checkbox';
                    new_check_unit.name = 'features';
                    new_check_unit.value = data.new_feature_unit.id;
                    new_check_unit.id = 'id_features_' + cantidad_unit;
                    new_check_unit.classList.add('form-check-input');
                    new_check_unit.checked = true;

                    new_label_unit.setAttribute('for', new_check_unit.id);
                    new_label_unit.classList.add('d-block');
                    new_label_unit.textContent = data.new_feature_unit.name;

                    new_label_unit.appendChild(new_check_unit);
                    // Agregar el nuevo checkbox al principio del contenedor
                    checkboxContainer_unit.appendChild(new_label_unit);
                    
                    // Cierra el modal
                    $('#Feature-unit-modal').modal('hide');
                } else {
                    // Manejar errores si es necesario
                }
            }
        });
    });
    

    // Función para cerrar el modal
    function closeModal() {
        $('#Feature-modal').modal('hide');
    }

    // Manejar la creación de un nuevo Tipo de Características
    document.getElementById("save-feature").addEventListener("click", function() {
        var typeInput = document.getElementById("id_type");
        var valueInput = document.getElementById("id_value");
        var typeValue = typeInput.value.trim();
        var valueValue = valueInput.value.trim();
        if (typeValue === "" || valueValue === "") {
            // Mostrar un mensaje de error o realizar alguna acción
            var errorElement = document.getElementById("error_feature");
            errorElement.textContent = "Ambos campos deben completarse.";
        } else {
            // Envía el formulario si los campos no están vacíos
            // Obtener el formulario dentro del modal personalizado
            var formData = new FormData(document.getElementById("Feature-form"));
            // Obtener los datos del formulario
            var errorMessage = document.getElementById('error_feature');
            errorMessage.textContent = '';
            
            var checkboxes = document.querySelectorAll('input[type="checkbox"][id^="id_features_"]');
            var uniqueCheckboxIDs = new Set();
            
            checkboxes.forEach(function(checkbox) {
                uniqueCheckboxIDs.add(checkbox.id);
            });
            
            var cantidad = uniqueCheckboxIDs.size;

            $.ajax({
                url: `/products/new/feature_full/`,
                method: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    if (data.status === 'success') {
                        var textSeparated = data.new_feature.name.trim().split(" - ");
    
                        let textButtonContainer = document.createElement('div');
                        textButtonContainer.classList.add('d-flex', 'align-items-center');
    
                        let addButton_new = document.createElement('span');
                        addButton_new.setAttribute('title','Agregar uno nuevo');
                        btnAdd.classList.add('fa-stack','ms-1','ms-sm-0');
                        btnAdd.style.fontSize = '.6em';
                        addButton_new.style.cursor = 'pointer';
                        addButton_new.innerHTML = `<i class="fas fa-circle fa-stack-2x text-primary"></i>
                        <i class="fa-inverse fa-stack-1x dark__text-white fas fa-plus"></i>`;
    
                        addButton_new.addEventListener('click', function() {
                            // Actualiza el título del modal con el tipo correspondiente
                            let modal = $('#Feature-unit-modal');
                            modal.find('.modal-title').text('Añade una nueva característica para ' + textSeparated[0]);
            
                            modal.modal('show');
            
                            // Obtén el campo de entrada con ID "id_type" dentro del formulario
                            let inputField = modal.find('#Feature-unit-form #id_type');
            
                            inputField.attr('type', 'hidden');
                            inputField.val(textSeparated[0]);
            
                            isModalOpen = true;
            
                            modal.on('hidden.bs.modal', function() {
                                isModalOpen = false;
                            });
                        });
    
                        let typeContainer = document.createElement('div');
                        typeContainer.classList.add('col-12','col-sm-6', 'col-md-3', 'pt-2');
                        let typeTittle = document.createElement('label');  
                        typeTittle.classList.add('mb-0','fw-bold');
                        
                        let checkboxContainer = document.createElement('div');
                        checkboxContainer.classList.add('col-md-12', 'mx-4', 'pt-1');
                        checkboxContainer.id = `${textSeparated[0]}`;
                        
                        let new_check = document.createElement('input');
                        let new_label = document.createElement('label');
                        
                        new_check.type = 'checkbox';
                        new_check.name = 'features';
                        new_check.id = 'id_features_' + cantidad;
                        new_check.value = data.new_feature.id;
                        new_check.classList.add('form-check-input');
                        new_check.checked = true;
                        
                        new_label.classList.add('d-block');
                        new_label.setAttribute('for', new_check.id);
                        new_label.textContent = textSeparated[1];
                        
                        typeTittle.textContent = textSeparated[0];
                        textButtonContainer.appendChild(typeTittle);
                        textButtonContainer.appendChild(addButton_new);
    
                        new_label.appendChild(new_check);
                        
                        checkboxContainer.appendChild(new_label);
    
                        typeContainer.appendChild(textButtonContainer);
                        typeContainer.appendChild(checkboxContainer);
                        typesContainer.appendChild(typeContainer);
            
                        closeModal(); // Cerrar el modal después de agregar el nuevo tipo
                    } else {
                        errorMessage.className = "text-danger text-center";
                        errorMessage.style.fontSize = "0.8rem";
                        errorMessage.textContent = data.error_message;
                    }
                }
            });
          }
    });
    
    const is_armazon = document.getElementById('id_is_armazon');
    const cost_price = document.getElementById("id_cost_price");
    const suggested_price = document.getElementById("id_suggested_price");
    const sale_price = document.getElementById("id_sale_price");

    let packaging = 580;
    let percentage_gral = parseFloat(1.26);
    let multiplicador = 3;

    is_armazon.addEventListener("change", function() {
        updatePrices();
    });

    cost_price.addEventListener("input", function() {
        updatePrices();
    });

    function updatePrices() {
        const costValue = parseFloat(cost_price.value);

        if (is_armazon.checked) {
            const final_price = parseFloat(suggested_price.textContent);
            const costWithExtra = parseFloat(final_price + packaging).toFixed(2);
            displaySuggestedPrice(costWithExtra);
            roundToNearest50(costWithExtra);
        } else {
            const cost = ((costValue * percentage_gral) * multiplicador).toFixed(2);
            displaySuggestedPrice(cost);
            roundToNearest50(cost);
        }
    }

    function displaySuggestedPrice(cost) {
        suggested_price.textContent = cost;
    }

    function roundToNearest50(cost) {
        const roundedSaleValue = Math.ceil(cost / 50) * 50;
        sale_price.value = roundedSaleValue.toFixed(2);
    }

});
