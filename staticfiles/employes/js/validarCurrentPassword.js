// Añadir un evento de escucha al campo de contraseña actual
$('#id_passwordCurrent').on('blur', function() {
	const currentPassword = $(this).val();

// Realizar la solicitud AJAX al servidor para validar la contraseña actual
	$.ajax({

		url: '{% url "employees_app:validate_current_password" %}',
		method: 'POST',
		data: { 'current_password': currentPassword },
		success: function(data) {
			if (!data.valid) {
				$('#password-error-message').text('La contraseña actual es incorrecta.');
			} else {
				$('#password-error-message').text('');
			}
		},
		error: function() {
			$('#password-error-message').text('Error de validación en el servidor.');
		}
	});
});