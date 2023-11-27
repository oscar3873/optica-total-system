#################### GESTIÓN DE USUARIOS #####################

**AdminProfileView:**

Esta vista muestra el perfil del administrador, incluyendo información sobre objetivos de empleados y objetivos de sucursales. Para los usuarios no administradores, también muestra los objetivos del empleado asociado.

- **Parámetros:**
  - `get_context_data`: Obtiene datos de contexto para la renderización de la vista.

**AdminCreateView:**

Esta vista permite la creación de un administrador mediante un formulario (`UserCreateForm`). Después de la creación, redirige al usuario a la página de inicio.

- **Parámetros:**
  - `form_valid`: Maneja la presentación del formulario cuando es válido.
  - `get_context_data`: Obtiene datos de contexto para la renderización de la vista.

**LoginView:**

Esta vista maneja la autenticación de usuarios. Utiliza el formulario `LoginForm` y redirige al usuario a la vista de punto de venta después de iniciar sesión. Para los administradores, la redirección es a la vista de resumen diario del panel de control.

- **Parámetros:**
  - `form_valid`: Maneja la presentación del formulario cuando es válido.
  - `dispatch`: Maneja la lógica antes de procesar la solicitud.

**LogoutView:**

Esta vista maneja la salida de sesión del usuario.

- **Parámetros:**
  - `get`: Procesa la solicitud de salida de sesión.

**AccountView:**

Esta vista permite la visualización y actualización de la información de la cuenta del usuario. Incluye información sobre las ventas realizadas por el usuario.

- **Parámetros:**
  - `form_valid`: Maneja la presentación del formulario cuando es válido.
  - `get_context_data`: Obtiene datos de contexto para la renderización de la vista.
  - `get_success_url`: Obtiene la URL de redirección después de una actualización exitosa.

**UpdatePasswordView:**

Esta vista permite el cambio de contraseña del usuario.

- **Parámetros:**
  - `form_valid`: Maneja la presentación del formulario cuando es válido.
  - `form_invalid`: Maneja la presentación del formulario cuando es inválido.

**UserChangeImagen:**

Esta vista permite cambiar la imagen de perfil del usuario.

- **Parámetros:**
  - `form_valid`: Maneja la presentación del formulario cuando es válido.
  - `get_success_url`: Obtiene la URL de redirección después de una actualización exitosa.
