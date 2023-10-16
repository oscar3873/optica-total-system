document.addEventListener("DOMContentLoaded", function () {
    const addFormButton = document.getElementById("add-form");
    const formsetForms = document.getElementById("formset-forms");
    const emptyForm = `{{ form.empty_form }}`;

    addFormButton.addEventListener("click", function () {
        // Clonar los formularios visibles
        const visibleForms = formsetForms.querySelectorAll(".visible-form");
        const count = visibleForms.length;
        const tmplMarkup = emptyForm.replace(/__prefix__/g, count);

        // Agregar el nuevo formulario clonado
        const newForm = document.createElement('div');
        newForm.className = 'visible-form';
        newForm.innerHTML = tmplMarkup;
        formsetForms.appendChild(newForm);

        // Actualizar el contador de formularios
        const totalFormsInput = document.querySelector("#id_form-TOTAL_FORMS");
        totalFormsInput.value = count + 1;
    });
    });