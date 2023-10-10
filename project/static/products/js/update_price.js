document.addEventListener("DOMContentLoaded", () => {
    const brandbutton = document.getElementById('choice_type_0');
    const categorybutton = document.getElementById('choice_type_1');
    const searchContainer = document.getElementById('search-contains');

    const searchInput = document.getElementById('search_term');
    const findResults = document.getElementById("search-results");
    const updateButton = document.getElementById('update-price-btn');
    const percentageContainer = document.getElementById('percentage-container'); // Agregado

    const selectedItemsList = []; // Array para almacenar elementos seleccionados

    function handleRadioButtonChange() {
        searchContainer.hidden = false;
        searchInput.value = "";
        findResults.innerHTML = "";
    }

    brandbutton.addEventListener('change', handleRadioButtonChange);
    categorybutton.addEventListener('change', handleRadioButtonChange);

    searchInput.addEventListener('input', () => {
        // Manejo del evento de entrada en el buscador
        const searchTerm = searchInput.value;
        const selectedOption = document.querySelector('input[type="radio"]:checked').value;
        const url_search = searchContainer.getAttribute('data-url');

        // Verificar si el campo de búsqueda está vacío
        if (searchTerm === "") {
            // Limpiar los resultados y deshabilitar el botón
            findResults.innerHTML = "";
            updateButton.disabled = true;
            return;
        }

        // Realizar una solicitud AJAX para buscar categorías o marcas
        $.ajax({
            url: url_search,
            data: {
                search_term: searchTerm,
                option: selectedOption,
            },
            success: function (data) {
                // Limpiar los resultados anteriores
                findResults.innerHTML = "";
                data.forEach(function (result) {
                    // Obtén la opción seleccionada
                    var selectedOption = document.querySelector('input[type="radio"]:checked').value;

                    // Crea un elemento de entrada de radio
                    var checkBtn = document.createElement("input");
                    checkBtn.type = "checkbox";
                    checkBtn.data = `${result.name}`;
                    checkBtn.value = result.id;

                    // Establece el nombre y el id según la opción seleccionada
                    if (selectedOption === 'brand') {
                        checkBtn.name = "brand";
                    } else {
                        checkBtn.name = "category";
                    }

                    // Verificar si el elemento ya está en la lista de seleccionados
                    const isSelected = selectedItemsList.some(item => item.data === checkBtn.data);
                    checkBtn.checked = isSelected;

                    checkBtn.addEventListener('change', (event) => {
                        const check = event.target;
                        if (check.checked) {
							console.log(check);
                            selectedItemsList.push(check); // Agregar el nuevo checkbox clonado a la lista
                            updateSelectedItemsList(); // Actualizar la lista visible
                            percentageContainer.hidden = false; // Mostrar el contenedor al seleccionar un elemento
                        } else {
                            const selectedIndex = selectedItemsList.findIndex(item => item.data === check.data);
                            if (selectedIndex !== -1) {
                                selectedItemsList.splice(selectedIndex, 1);
                                updateSelectedItemsList(); // Actualizar la lista visible
                            }

                            // Deseleccionar el checkbox correspondiente en la lista de resultados
                            const checkboxesInResults = document.querySelectorAll('#search-results input[type="checkbox"]');
                            checkboxesInResults.forEach((checkbox) => {
                                if (checkbox.data === check.data) {
                                    checkbox.checked = false;
                                }
                            });

                            // Ocultar el contenedor si no hay elementos seleccionados
                            if (selectedItemsList.length === 0) {
                                percentageContainer.hidden = true;
                            }
                        }
                    });

                    // Crea un elemento de etiqueta
                    var label = document.createElement("label");
                    label.textContent = result.name;
                    label.htmlFor = result.name;

                    // Obtén el contenedor de resultados
                    var searchResults = document.getElementById("search-results");

                    // Agrega los elementos al contenedor
                    searchResults.appendChild(checkBtn);
                    searchResults.appendChild(label);
                    searchResults.appendChild(document.createElement("br"));
                });

                updateButton.disabled = false;
            },
            error: function () {
                updateButton.disabled = true;
            },
        });
    });

    // Función para actualizar la lista visible de elementos seleccionados
    function updateSelectedItemsList() {
        const selectedItemsContainer = document.getElementById('selected-items-list');
        selectedItemsContainer.innerHTML = ""; // Limpiar la lista

        selectedItemsList.forEach((item) => {
            var selectedOption = document.querySelector('input[type="radio"]:checked').value;

            const checkBtn = document.createElement('input');
            checkBtn.type = 'checkbox';
            checkBtn.checked = true; // Marcar el checkbox como seleccionado
            checkBtn.value = item.value;
            checkBtn.data = item.data;
			checkBtn.name = item.name;

            checkBtn.addEventListener('change', (event) => {
                const check = event.target;
                if (check.checked) {
                    selectedItemsList.push(check); // Agregar el nuevo checkbox clonado a la lista
                    updateSelectedItemsList(); // Actualizar la lista visible
                } else {
                    const selectedIndex = selectedItemsList.findIndex(item => item.data === check.data);
                    if (selectedIndex !== -1) {
                        selectedItemsList.splice(selectedIndex, 1);
                        updateSelectedItemsList(); // Actualizar la lista visible
                    }

                    // Deseleccionar el checkbox correspondiente en la lista de resultados
                    const checkboxesInResults = document.querySelectorAll('#search-results input[type="checkbox"]');
                    checkboxesInResults.forEach((checkbox) => {
                        if (checkbox.data === check.data) {
                            checkbox.checked = false;
                        }
                    });

                    // Ocultar el contenedor si no hay elementos seleccionados
                    if (selectedItemsList.length === 0) {
                        percentageContainer.hidden = true;
                    }
                }
            });

            selectedItemsContainer.appendChild(checkBtn);

            const label = document.createElement('label');
            label.textContent = item.data;
            selectedItemsContainer.appendChild(label);

            selectedItemsContainer.appendChild(document.createElement('br')); // Agregar un salto de línea entre los checkboxes
        });
    }
});
