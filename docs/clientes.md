#################################### CREATE ####################################
class ServiceOrderCreateView(LoginRequiredMixin, FormView):
    """
    Vista para la creación de nuevas órdenes de servicio.

    Lógica:
    - Se crea una nueva orden de servicio con formularios adicionales para detalles específicos.
    - Se asocia la orden de servicio con un cliente existente.

    Validación:
    - Se verifica que el usuario esté autenticado para crear una orden de servicio.
    """

    # Lógica detallada de la vista:
    1. Recibe la información del formulario principal y formularios adicionales.
    2. Asocia la orden de servicio con un cliente existente.
    3. Guarda la nueva orden de servicio y sus detalles en la base de datos.
    4. Maneja errores y redirige a la página de detalle del cliente.

#################################### UPDATE ####################################
class ServiceOrderUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para la actualización de una orden de servicio existente.

    Lógica:
    - Se actualizan los datos de la orden de servicio y sus detalles asociados.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para actualizar la orden de servicio.
    """

    # Lógica detallada de la vista:
    1. Recibe la información del formulario principal y formularios adicionales.
    2. Asocia la orden de servicio con un cliente existente.
    3. Actualiza los datos de la orden de servicio y sus detalles en la base de datos.
    4. Maneja errores y redirige a la página de detalle del cliente.

################################## LISTING  ##################################
class CustomerListView(LoginRequiredMixin, ListView):
    """
    Vista para listar los clientes disponibles.

    Lógica:
    - Se filtran los clientes por la sucursal actual del usuario.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la lista de clientes.
    """

    # Lógica detallada de la vista:
    1. Filtra los clientes por la sucursal actual del usuario.
    2. Presenta la lista de clientes disponibles.

########################### DELETE ####################################

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar un cliente existente.

    Lógica:
    - Desactiva el cliente y realiza una eliminación suave.
    - Elimina el registro del cliente.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la vista de eliminación.
    """

    # Lógica detallada de la vista:
    1. Desactiva el cliente y realiza una eliminación suave.
    2. Elimina el registro del cliente.
    3. Maneja errores y redirige a la página de lista de clientes.


#################################### UPDATE ####################################
class HealthInsuranceUpdateView(CustomUserPassesTestMixin, UpdateView):
    """
    Vista para la actualización de datos de una obra social existente.

    Lógica:
    - Actualiza los datos de la obra social con la información proporcionada en el formulario.

    Validación:
    - Se verifica que el formulario sea válido antes de realizar la actualización.
    """

    # Lógica detallada de la vista:
    1. Recibe la información del formulario de obra social.
    2. Asocia la obra social con el usuario que realiza la actualización.
    3. Actualiza los datos de la obra social en la base de datos.
    4. Maneja errores y redirige a la página de lista de obras sociales.

############################## DETAIL ##############################

class CustomerDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para visualizar el detalle de un cliente.

    Lógica:
    - Verifica que el usuario tenga permisos para ver el cliente.
    - Muestra el perfil del cliente, incluyendo órdenes de servicio y detalles de ventas asociados.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder al detalle del cliente.
    """

    # Lógica detallada de la vista:
    1. Verifica los permisos del usuario para ver el cliente.
    2. Muestra el perfil del cliente, incluyendo órdenes de servicio y detalles de ventas asociados.

    def get(self, request, *args, **kwargs):
        # ... (implementación detallada del método)

    def get_context_data(self, **kwargs):
        # ... (implementación detallada del método)

class ServiceOrderDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para visualizar el detalle de una orden de servicio.

    Lógica:
    - Muestra el detalle de una orden de servicio, incluyendo información relevante.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder al detalle de la orden de servicio.
    """

    # Lógica detallada de la vista:
    1. Muestra el detalle de una orden de servicio, incluyendo información relevante.

class HealthInsuranceDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para visualizar el detalle de una obra social.

    Lógica:
    - Muestra el detalle de una obra social, incluyendo información relevante.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder al detalle de la obra social.
    """

    # Lógica detallada de la vista:
    1. Muestra el detalle de una obra social, incluyendo información relevante.

############################## LISTING ###############################

class CustomerListView(LoginRequiredMixin, ListView):
    """
    Vista para listar los clientes disponibles.

    Lógica:
    - Filtra los clientes por la sucursal actual del usuario.
    - Presenta la lista de clientes disponibles.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la lista de clientes.
    """

    # Lógica detallada de la vista:
    1. Filtra los clientes por la sucursal actual del usuario.
    2. Presenta la lista de clientes disponibles.

    def get_context_data(self, **kwargs):
        # ... (implementación detallada del método)

    def get_queryset(self):
        # ... (implementación detallada del método)

class ServiceOrderListView(LoginRequiredMixin, ListView):
    """
    Vista para listar las órdenes de servicio disponibles.

    Lógica:
    - Presenta la lista de órdenes de servicio disponibles.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la lista de órdenes de servicio.
    """

    # Lógica detallada de la vista:
    1. Presenta la lista de órdenes de servicio disponibles.

class HealthInsuranceListView(LoginRequiredMixin, ListView):
    """
    Vista para listar las obras sociales disponibles.

    Lógica:
    - Presenta la lista de obras sociales disponibles.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la lista de obras sociales.
    """

    # Lógica detallada de la vista:
    1. Presenta la lista de obras sociales disponibles.


#################################### CREATE ####################################
class ServiceOrderCreateView(LoginRequiredMixin, FormView):
    """
    Vista para la creación de nuevas órdenes de servicio.

    Lógica:
    - Se crea una nueva orden de servicio con formularios adicionales para detalles específicos.
    - Se asocia la orden de servicio con un cliente existente.

    Validación:
    - Se verifica que el usuario esté autenticado para crear una orden de servicio.
    """

    # Lógica detallada de la vista:
    1. Recibe la información del formulario principal y formularios adicionales.
    2. Asocia la orden de servicio con un cliente existente.
    3. Guarda la nueva orden de servicio y sus detalles en la base de datos.
    4. Maneja errores y redirige a la página de detalle del cliente.

#################################### UPDATE ####################################
class ServiceOrderUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para la actualización de una orden de servicio existente.

    Lógica:
    - Se actualizan los datos de la orden de servicio y sus detalles asociados.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para actualizar la orden de servicio.
    """

    # Lógica detallada de la vista:
    1. Recibe la información del formulario principal y formularios adicionales.
    2. Asocia la orden de servicio con un cliente existente.
    3. Actualiza los datos de la orden de servicio y sus detalles en la base de datos.
    4. Maneja errores y redirige a la página de detalle del cliente.

################################## LISTING  ##################################
class CustomerListView(LoginRequiredMixin, ListView):
    """
    Vista para listar los clientes disponibles.

    Lógica:
    - Se filtran los clientes por la sucursal actual del usuario.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la lista de clientes.
    """

    # Lógica detallada de la vista:
    1. Filtra los clientes por la sucursal actual del usuario.
    2. Presenta la lista de clientes disponibles.

########################### DELETE ####################################

class ServiceOrderDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar una orden de servicio existente.

    Lógica:
    - Elimina la orden de servicio y sus detalles asociados.
    - Maneja redireccionamiento después de la eliminación.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la vista de eliminación.
    """

    # Lógica detallada de la vista:
    1. Obtiene el cliente asociado a la orden de servicio antes de la eliminación.
    2. Elimina la orden de servicio y sus detalles.
    3. Maneja redireccionamiento a la página de detalle del cliente.

class CustomerDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar un cliente existente.

    Lógica:
    - Elimina el cliente y las relaciones asociadas, como seguros de salud.
    - Maneja redireccionamiento después de la eliminación.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la vista de eliminación.
    """

    # Lógica detallada de la vista:
    1. Obtiene el cliente antes de la eliminación.
    2. Elimina el cliente y relaciones asociadas, como seguros de salud.
    3. Maneja redireccionamiento a la página de lista de clientes.

class HealthInsuranceDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar un seguro de salud existente.

    Lógica:
    - Elimina el seguro de salud y las relaciones asociadas con clientes.
    - Maneja redireccionamiento después de la eliminación.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la vista de eliminación.
    """

    # Lógica detallada de la vista:
    1. Obtiene el seguro de salud antes de la eliminación.
    2. Elimina el seguro de salud y relaciones asociadas con clientes.
    3. Maneja redireccionamiento a la página de lista de seguros de salud.

####################### CREDIT ACCOUNT #######################

def open_credit_account(request, pk):
    """
    Vista para abrir una cuenta corriente para un cliente.

    Lógica:
    - Verifica si el cliente ya tiene una cuenta corriente abierta.
    - Abre una nueva cuenta corriente si no existe.
    - Maneja redireccionamiento después de la apertura.

    Validación:
    - Se verifica que el usuario esté autenticado.
    """

    # Lógica detallada de la vista:
    1. Obtiene el cliente.
    2. Verifica si el cliente ya tiene una cuenta


#################################### DELETE ####################################
class ServiceOrderDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar una orden de servicio existente.

    Lógica:
    - Obtiene el contexto para la plantilla de eliminación, incluyendo información sobre el cliente asociado.
    - Define la URL de redirección después de la eliminación.

    Validación:
    - Utiliza un mixin personalizado para verificar si el usuario tiene permisos.

    # Lógica detallada de la vista:
    1. Obtiene el contexto para la plantilla de eliminación, incluyendo información sobre el cliente asociado.
    2. Define la URL de redirección después de la eliminación.
    3. Utiliza un mixin personalizado para verificar si el usuario tiene permisos.

    # Métodos relevantes:
    - get_context_data: Obtiene y retorna el contexto para la plantilla de eliminación, incluyendo información sobre el cliente asociado.
    - get_success_url: Retorna la URL de redirección después de la eliminación de una orden de servicio.

#################################### DELETE ####################################
class CustomerDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar un cliente existente.

    Lógica:
    - Desactiva el cliente y realiza una eliminación suave.
    - Elimina el registro del cliente.

    Validación:
    - Utiliza un mixin personalizado para verificar si el usuario tiene permisos.

    # Lógica detallada de la vista:
    1. Desactiva el cliente y realiza una eliminación suave.
    2. Elimina el registro del cliente.
    3. Maneja errores y redirige a la página de lista de clientes.

    # Métodos relevantes:
    - delete: Elimina un cliente. Realiza validaciones para evitar la eliminación de clientes especiales.

#################################### DELETE ####################################
class HealthInsuranceDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar un seguro de salud existente.

    Lógica:
    - Elimina el seguro de salud y las relaciones asociadas con clientes.
    - Define la URL de redirección después de la eliminación.

    Validación:
    - Utiliza un mixin personalizado para verificar si el usuario tiene permisos.

    # Lógica detallada de la vista:
    1. Elimina el seguro de salud y las relaciones asociadas con clientes.
    2. Define la URL de redirección después de la eliminación.
    3. Utiliza un mixin personalizado para verificar si el usuario tiene permisos.

    # Métodos relevantes:
    - delete: Elimina un seguro de salud. Elimina relaciones con clientes antes de eliminar el seguro.

################################ DELETE ################################
class open_credit_account:
    """
    Vista para abrir una cuenta corriente para un cliente.

    Lógica:
    - Verifica si el cliente ya tiene una cuenta corriente abierta y, si no, la abre.

    Validación:
    - Utiliza un formulario HTTP POST.

    # Lógica detallada de la vista:
    1. Verifica si el cliente ya tiene una cuenta corriente abierta y, si no, la abre.

    # Métodos relevantes:
    - open_credit_account: Abre una cuenta corriente para un cliente.

################################ DELETE ################################
class pay_credits:
    """
    Vista para realizar el pago de una cuenta corriente del cliente.

    Lógica:
    - Realiza validaciones y crea un registro de movimiento de ingreso en la caja registradora.

    Validación:
    - Utiliza un formulario HTTP POST.

    # Lógica detallada de la vista:
    1. Realiza validaciones y crea un registro de movimiento de ingreso en la caja registradora.

    # Métodos relevantes:
    - pay_credits: Realiza el pago de una cuenta corriente del cliente.

################################ DELETE ################################
class close_credit_account:
    """
    Vista para cerrar la cuenta corriente de un cliente.

    Lógica:
    - Solo puede ser ejecutada por administradores.

    Validación:
    - Verifica si el usuario es un administrador.

    # Lógica detallada de la vista:
    1. Solo puede ser ejecutada por administradores.

    # Métodos relevantes:
    - close_credit_account: Cierra la cuenta corriente de un cliente.

################################ DELETE ################################
class export_order_service_list_to_excel:
    """
    Vista para exportar las órdenes de servicio de un cliente a un archivo Excel.

    Lógica:
    - Genera un archivo Excel con información detallada sobre las órdenes de servicio del cliente.

    Validación:
    - Verifica si el cliente tiene órdenes de servicio antes de la exportación.

    # Lógica detallada de la vista:
    1. Genera un archivo Excel con información detallada sobre las órdenes de servicio del cliente.

    # Métodos relevantes:
    - export_order_service_list_to_excel: Exporta órdenes de servicio a un archivo Excel.

################################ DELETE ################################
class pay_service_order:
    """
    Vista para realizar el pago de una orden de servicio.

    Lógica:
    - Realiza validaciones y crea un registro de movimiento de ingreso en la caja registradora.

    Validación:
    - Utiliza un formulario HTTP POST.

    # Lógica detallada de la vista:
    1. Realiza validaciones y crea un registro de movimiento de ingreso en la caja registradora.

    # Métodos relevantes:
    - pay_service_order: Realiza el pago de una orden de servicio.

################################ PRINT SERVICE ORDER ################################
def print_service_order(request, pk):
    """
    Vista para imprimir una orden de servicio.

    Lógica:
    - Verifica que la solicitud sea una petición AJAX y de método GET.
    - Obtiene la orden de servicio por su clave primaria (pk).
    - Genera un contenido HTML personalizado con la información de la orden de servicio y la fecha de venta.
    - Devuelve el HTML como respuesta.

    Validación:
    - Verifica que la solicitud sea una petición AJAX y de método GET.

    # Lógica detallada de la vista:
    1. Verifica que la solicitud sea una petición AJAX y de método GET.
    2. Obtiene la orden de servicio por su clave primaria (pk).
    3. Genera un contenido HTML personalizado con la información de la orden de servicio y la fecha de venta.
    4. Devuelve el HTML como respuesta.

    # Métodos relevantes:
    - print_service_order: Imprime una orden de servicio en formato HTML.

################################ SERVICE ORDER ENTREGA ################################
def service_order_entrega(request, pk):
    """
    Vista para marcar una orden de servicio como entregada.

    Lógica:
    - Verifica que la solicitud sea una petición POST.
    - Obtiene la orden de servicio por su clave primaria (pk).
    - Marca la orden de servicio como entregada.
    - Muestra un mensaje de éxito.
    - Redirige a la página de detalles del cliente asociado.

    Validación:
    - Verifica que la solicitud sea una petición POST.

    # Lógica detallada de la vista:
    1. Verifica que la solicitud sea una petición POST.
    2. Obtiene la orden de servicio por su clave primaria (pk).
    3. Marca la orden de servicio como entregada.
    4. Muestra un mensaje de éxito.
    5. Redirige a la página de detalles del cliente asociado.

    # Métodos relevantes:
    - service_order_entrega: Marca una orden de servicio como entregada.
