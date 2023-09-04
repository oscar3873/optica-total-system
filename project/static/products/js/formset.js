$(document).ready(function() {
    // Function to agregar un nuevo formulario de variante
    function addVariantForm() {
        var count = $('#item-variants').children().length;
        var tmplMarkup = $('#variants-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('#item-variants').append(compiledTmpl);

        // Actualizar el contador de formularios
        $('#id_variants-TOTAL_FORMS').attr('value', count + 1);

        // Agregar el botón "Agregar Valor" al nuevo formulario de variante
        var newForm = $('#item-variants').children().last();
        var addValueButton = $('<button type="button" class="btn btn-secondary add-value">Agregar Valor</button>');
        addValueButton.appendTo(newForm.find('td:last'));

        // Manejar el clic en el botón "Agregar Valor"
        addValueButton.click(function(e) {
            e.preventDefault();
            addVariantForm(); // Agregar un nuevo formulario de variante

            // Ocultar el campo de entrada "Tipo" en el nuevo formulario
            var newForm = $('#item-variants').children().last();
            newForm.find('input[name$="-type"]').hide();

            // Copiar el texto del campo "Tipo" original al campo "Tipo" oculto del nuevo formulario
            var originalType = newForm.prev().find('input[name$="-type"]');
            var newType = newForm.find('input[name$="-type"]');
            newType.val(originalType.val());
        });
    }

    // Función para manejar el clic en el botón "Eliminar"
    function handleDeleteVariant() {
        var row = $(this).closest('tr');

        // Borrar el texto en los campos "Tipo" y "Valor"
        row.find('input[name$="-type"]').val('');
        row.find('input[name$="-value"]').val('');

        // Eliminar la fila
        row.remove();
    }

    // Adjuntar el controlador de clic inicial para el botón "Agregar Variante"
    $('.add-variants').click(function(ev) {
        ev.preventDefault();
        addVariantForm();
    });

    // Adjuntar el controlador de clic en el botón "Eliminar" a las variantes existentes
    $(document).on('click', '.delete-variant', handleDeleteVariant);
});
