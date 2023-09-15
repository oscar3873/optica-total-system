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
        typeContainer.classList.add('col-6', 'col-md-2');

        let typeTitle = document.createElement('h5');
        typeTitle.textContent = `${type}`;

        // Contenedor que alinea horizontalmente el h5 y el botón
        let textButtonContainer = document.createElement('div');
        textButtonContainer.classList.add('d-flex', 'align-items-center');

        // Contenedor de los checkboxes
        let checkboxContainer_unit = document.createElement('div');
        checkboxContainer_unit.classList.add('col-md-12', 'mx-4', 'pt-2');
        checkboxContainer_unit.id = `${type}`;

        textButtonContainer.appendChild(typeTitle);

        typeContainer.appendChild(textButtonContainer);

        // Agregar botón "+" y manejar su evento
        let addButton = document.createElement('button');
        addButton.textContent = '+';
        addButton.type = 'button';
        addButton.classList.add('btn', 'btn-sm', 'ml-2'); // Agregar 'ml-2' para espacio a la izquierda

        addButton.addEventListener('click', function() {
            if (!isModalOpen) {
                // Actualiza el título del modal con el tipo correspondiente
                let modal = $('#Feature-unit-modal');
                modal.find('.modal-title').text('Añade una nueva característica para ' + type);

                // Abre el modal
                modal.modal('show');

                // Obtén el campo de entrada con ID "id_type" dentro del formulario
                let inputField = modal.find('#Feature-unit-form #id_type');

                inputField.attr('type', 'hidden');
                inputField.val(type);

                // Marca el modal como abierto
                isModalOpen = true;

                // Configura el evento para cerrar el modal
                modal.on('hidden.bs.modal', function() {
                    isModalOpen = false;
                });
            }
        });

        // Agrega el botón "+" al título del Tipo de Característica
        textButtonContainer.appendChild(addButton);

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

        typeContainer.appendChild(textButtonContainer);
        typeContainer.appendChild(checkboxContainer_unit);
        typesContainer.appendChild(typeContainer);
    }

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
                    console.log(type);
    
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
                    checkboxContainer_unit.append(new_label_unit);
                    
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
        var formData = new FormData(document.getElementById("Feature-form"));
        var errorMessage = document.getElementById('error_feature');
        errorMessage.textContent = '';

        var cantidad = document.querySelectorAll('[id^="id_features_"]').length;

        $.ajax({
            url: `/products/new/feature_full/`,
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                if (data.status === 'success') {
                    let typeContainer = document.createElement('div');
                    typeContainer.classList.add('col-6', 'col-md-2', 'pb-3');
                    let typeTittle = document.createElement('h5');
                    var textSeparated = data.new_feature.name.trim().split(" - ");

                    typeTittle.textContent = textSeparated[0];
                    typeContainer.appendChild(typeTittle);

                    let checkboxContainer = document.createElement('div');
                    checkboxContainer.classList.add('col-md-12', 'mx-4', 'pt-2');

                    let new_check = document.createElement('input');
                    let new_label = document.createElement('label');

                    new_check.type = 'checkbox';
                    new_check.id = 'id_features_' + cantidad;
                    new_check.value = data.new_feature.id;
                    new_check.classList.add('form-check-input');
                    new_check.checked = true;

                    new_label.classList.add('d-block');
                    new_label.setAttribute('for', new_check.id);
                    new_label.textContent = textSeparated[1];

                    new_label.appendChild(new_check);
                    checkboxContainer.appendChild(new_label);
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
    });
});
