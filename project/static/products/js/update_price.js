$(document).ready(function () {
	// Ocultar el contenedor del campo de búsqueda inicialmente
	var searchContainer = $("#search-container");
	searchContainer.hide();
	// Url que viene del div de busqueda de busqueda en el parametro data-url 
	var url_search = searchContainer.data("url");

	// Ocultar el input de porcentaje al cargar la página
	$('.percentage-input').hide();

	// Deshabilitar el botón de actualización de precios al cargar la página
	$('#update-price-btn').prop('disabled', true);

	// Variable para rastrear si se ha seleccionado una opción de la lista de resultados
	var optionSelected = false;
	// Variable para almacenar la opción anteriormente seleccionada
	var previousOption = $('input[type="radio"]:checked').val();
	
	// Función para mostrar u ocultar el campo de búsqueda según la opción seleccionada
	function toggleSearchField() {
			var selectedOption = $('input[type="radio"]:checked').val();
			
			if (selectedOption === "brand" || selectedOption === "category") {
					$("#search-container").show(); // Mostrar el campo de búsqueda
			} else {
					$("#search-container").hide(); // Ocultar el campo de búsqueda
			}
	}
	// Función para redondear al múltiplo de 50 más cercano y limitar a 2 decimales
	function roundToNearest50(value) {
			return Math.round(value / 50) * 50;
	}
	
	// Función para mostrar u ocultar el input de porcentaje
	function togglePercentageInput() {
			if (optionSelected) {
					$('.percentage-input').show();
			} else {
					$('.percentage-input').hide();
			}
	}

	// Manejo del evento de cambio en la opción seleccionada
	$('input[type="radio"]').change(function () {
			toggleSearchField();
			// Obtén la nueva opción seleccionada
			var selectedOption = $(this).val();

			// Verificar si la opción seleccionada ha cambiado
			if (selectedOption !== previousOption) {
					// Limpiar el campo de búsqueda y los resultados anteriores
					$("#search").val("");
					$("#search-results").empty();
					// Actualizar la opción anteriormente seleccionada
					previousOption = selectedOption;
			}

			// Mostrar u ocultar el buscador según la opción seleccionada
			if (selectedOption === "brand" || selectedOption === "category") {
					$("#search").show(); // Mostrar el buscador
			} else {
					$("#search").hide(); // Ocultar el buscador
			}
	});

	// Manejo del evento de entrada en el buscador
	$("#search").on("input", function () {
			var searchTerm = $(this).val();
			var selectedOption = $('input[type="radio"]:checked').val();

			// Verificar si el campo de búsqueda está vacío
			if (searchTerm === "") {
					// Limpiar los resultados y deshabilitar el botón
					$("#search-results").empty();
					$('#update-price-btn').prop('disabled', true);
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
							$("#search-results").empty();

							// Mostrar los nuevos resultados como botones de radio
							$.each(data, function (index, result) {

									var selectedOption = $('input[type="radio"]:checked').val();
									var container_item = $('<div class="option-item"></div>')
									var radioBtn = $(
									'<input type="radio" name="selected_category_or_brand">'
									)
									.attr("value", result.id).attr("id",result.name).attr("class","form-radius-check")
									.appendTo($("#search-results"));
									if (selectedOption == 'brand'){
											radioBtn.attr("name","brand").attr("id","id_search_type_brand")
									}else{
											radioBtn.attr("name","category").attr("id","id_search_type_category")
											// poner el input radio para categoria
									}
									$("<label>").text(result.name)
									.attr("for",result.name)
									.appendTo($("#search-results"));
									$("#search-results").append("<br>");
							});

							// Habilitar el botón si se muestran resultados
							$('#update-price-btn').prop('disabled', false);
					},
					error: function () {
					// Manejar errores, si es necesario
					},
			});
	});
	
	 // Manejo del evento de clic en un elemento de la lista de resultados
	$('#search-results').on('change', 'input[type="radio"]', function() {
			// Verifica si se ha seleccionado un elemento
			if ($(this).is(':checked')) {
					optionSelected = true;
			} else {
					optionSelected = false;
			}
			// Muestra u oculta el input de porcentaje según si se selecciona un elemento
			togglePercentageInput();
	});
	
	// Manejo del evento de clic en el botón de actualización de precios
	$("#update-price-btn").click(function () {
			
	});
});
