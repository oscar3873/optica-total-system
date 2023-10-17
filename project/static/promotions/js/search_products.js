document.addEventListener("DOMContentLoaded", function () {
    
    function configureSearch(searchInput, searchResults, fieldIdentifier) {
        searchInput.addEventListener('input', (event) => {
            const searchTerm = event.target.value.trim().toLowerCase();

            if (!searchTerm) {
                // Limpiar los resultados de búsqueda si no hay término de búsqueda
                searchResults.innerHTML = '';
                return;
            }

            // Realizar la búsqueda de productos que coincidan con el término de búsqueda
            $.ajax({
                url: `/products/ajax_search_products/?search_term=${searchTerm}`,
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    const products = data.data;

                    // Mostrar los resultados de búsqueda
                    searchResults.innerHTML = ''; // Limpia los resultados anteriores

                    products.forEach(product => {
                        const item = document.createElement('li');
                        item.style.zIndex = "9999";
                        item.style.cursor = 'pointer';
                        item.classList.add('list-group-item', 'products');
                        item.dataset.productId = product.id;
                        item.innerHTML = `
                            <div class="d-flex justify-content-between">
                                <h6>${product.name}</h6>
                                <h6 class="font-weight-bold">&nbsp${product.barcode}</h6>
                            </div>
                        `;
                        searchResults.appendChild(item);
                    });
                },
                error: function(error) {
                    console.error('Error en la solicitud AJAX', error);
                }
            });
        });

        searchResults.addEventListener('click', (event) => {
            const item = event.target.closest('.products');
            if (!item) {
                return;
            }

            const productId = item.dataset.productId;
            const productName = item.querySelector('h6').textContent;

            // Rellenar el campo del producto seleccionado y ocultar los resultados de búsqueda
            searchInput.value = productName;
            searchResults.innerHTML = '';

            // Añadir el ID del producto al formulario
            const productIdCheck = document.createElement('input');
            productIdCheck.type = 'hidden';
            productIdCheck.name = `selected_product_id_${fieldIdentifier}`;
            productIdCheck.value = productId;
            searchInput.closest('form').appendChild(productIdCheck);
        });
    }

    function addForm() {
        const name_0 = document.getElementById('id_form-0-name');
        const description_0 = document.getElementById('id_form-0-description');
        const start_date_0 = document.getElementById('id_form-0-start_date');
        const end_date_0 = document.getElementById('id_form-0-end_date');

        const visibleForms = formsetForms.querySelectorAll(".visible-form");
        const count = visibleForms.length;
        const tmplMarkup = emptyForm.replace(/__prefix__/g, count);

        // Crear un nuevo formulario clonado
        const newForm = document.createElement('div');
        newForm.className = 'visible-form';
        newForm.id = `id_form-${count}`;
        newForm.innerHTML = tmplMarkup;
        formsetForms.appendChild(newForm);

        const newName = newForm.querySelector(`#${newForm.id}-name`);
        const newDescription = newForm.querySelector(`#${newForm.id}-description`);
        const newStart_date = newForm.querySelector(`#${newForm.id}-start_date`);
        const newEnd_date = newForm.querySelector(`#${newForm.id}-end_date`);

        newName.value = name_0.value;
        newDescription.value = description_0.value;
        newStart_date.value = start_date_0.value;
        newEnd_date.value = end_date_0.value;

        // Configurar los buscadores A y B en el nuevo formulario
        configureSearchInputs(newForm, count);
        configureDeleteButton(newForm);
        updateFormsetFormCount(count);
    }

    function configureSearchInputs(form, count) {
        const fieldPrefix = `id_form-${count}`;
        const searchInputA = form.querySelector(`#${fieldPrefix}-search-productA-input`);
        const searchResultsA = form.querySelector(`#${fieldPrefix}-search-productA-results`);
        const searchInputB = form.querySelector(`#${fieldPrefix}-search-productB-input`);
        const searchResultsB = form.querySelector(`#${fieldPrefix}-search-productB-results`);

        configureSearch(searchInputA, searchResultsA, 'productA');
        configureSearch(searchInputB, searchResultsB, 'productB');
    }

    function configureDeleteButton(form) {
        const deleteButton = document.createElement('button');
        deleteButton.type = "button";
        deleteButton.className = "delete-form";
        deleteButton.textContent = "Eliminar";
        deleteButton.addEventListener('click', function() {
            form.remove();
            updateFormFields();
        });
        form.appendChild(deleteButton);
    }

    function updateFormsetFormCount(count) {
        const totalFormsInput = document.querySelector("#id_form-TOTAL_FORMS");
        totalFormsInput.value = count + 1;
    }

    function updateFormFields() {
        const forms = formsetForms.querySelectorAll(".visible-form");
        forms.forEach((form, index) => {
            const fieldPrefix = `id_form-${index}`;
            form.id = fieldPrefix;
    
            console.log(form);
    
            const formChildren = Array.from(form.children);
    
            formChildren.forEach(child => {
                if (child.tagName === "DIV") {
                    const fields = child.querySelectorAll('[name^="form-"]');
                    fields.forEach(field => {
                        const fieldName = field.getAttribute("name");
                        const newFieldName = fieldName.replace(/form-\d+-/, `form-${index}-`);
                        field.setAttribute("name", newFieldName);
    
                        const fieldId = field.getAttribute("id");
                        const newFieldId = fieldId.replace(/id_form-\d+-/, `id_form-${index}-`);
                        field.setAttribute("id", newFieldId);
                    });
                }
            });
        });
    
        updateFormsetFormCount(forms.length);
    }
    

    const addFormButton = document.getElementById("add-form");
    const formsetForms = document.getElementById("formset-forms");
    const formulario = document.getElementById("form-hidden").getAttribute("data-form");

    const new_hidden_form = document.createElement("div");
    new_hidden_form.innerHTML = formulario;
    new_hidden_form.hidden = true;

    const emptyForm = `
        ${new_hidden_form.outerHTML}
        <div class="form-group">
            <input required type="text" id="id_form-__prefix__-search-productA-input" class="form-control rounded p-3 box-shadow" placeholder="Buscar producto A">
            <ul id="id_form-__prefix__-search-productA-results" class="list-group text-dark mt-3"></ul>
        </div>

        <div class="form-group">
            <input required type="text" id="id_form-__prefix__-search-productB-input" class="form-control rounded p-3 box-shadow" placeholder="Buscar producto B">
            <ul id="id_form-__prefix__-search-productB-results" class="list-group text-dark mt-3"></ul>
        </div>`;

    addFormButton.addEventListener("click", addForm);

    const form_0 = document.getElementById('id_form-0');
    configureSearchInputs(form_0, 0);
});
