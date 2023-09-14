document.addEventListener('DOMContentLoaded', function() {
    let typesContainer = document.getElementById('types-container');
    typesContainer.classList.add('d-flex');
    let checkboxes = document.getElementsByName("features");
    var typeSet = new Set();
    checkboxes.forEach(function(checkbox) {
        var textSeparated = checkbox.parentElement.textContent.trim().split(" - ");
        typeSet.add(textSeparated[0]);
    });
    
    for (let type of typeSet){
        //Contenedor del tipo
        let typeContainer = document.createElement('div');
        typeContainer.classList.add('d-flex', 'flex-column', 'mx-3');
        let typeTittle = document.createElement('h5');
        typeTittle.textContent = `${type}`;
        typeContainer.appendChild(typeTittle);
        //Contenedor de los checkbox
        let checkboxContainer = document.createElement('div');
        checkboxContainer.classList.add('d-flex', 'flex-column', 'mx-4', 'pt-2' );
        for (let checkbox of checkboxes) {
            let labelElement = checkbox.parentElement;
            let textLabel = labelElement.textContent.trim();
            let textSeparated = textLabel.split(" - ");
            let textType = textSeparated[0];
            let labelClon = labelElement.cloneNode(true);
            let inputClon = labelClon.firstElementChild;
            labelClon.textContent = textSeparated[1];
            labelClon.appendChild(inputClon);
            if(textType == type){
                checkboxContainer.appendChild(labelClon);
            }
        }
        typeContainer.appendChild(checkboxContainer);
        typesContainer.appendChild(typeContainer);
    }
   
   
    // Obtén una referencia al formulario por su ID o de alguna otra manera
    var form = document.getElementById('create-product');
    // Agrega un evento 'keydown' al formulario
    form.addEventListener('keydown', function(event) {
        // Verifica si la tecla presionada es 'Enter'
        if (event.key === 'Enter') {
            // Previene el comportamiento predeterminado del formulario (envío)
            event.preventDefault();
        }
    });


    var formCategory = document.getElementById('Product-category-modal');
    formCategory.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });

    var formBrand = document.getElementById('Product-brand-modal');
    formBrand.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });



    
});