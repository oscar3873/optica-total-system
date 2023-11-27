class PointOfSaleView(LoginRequiredMixin, FormView):
    """
    Vista para gestionar las ventas en un Punto de Venta (PoS).

    Lógica:
    - Requiere autenticación de usuario.
    - Verifica la existencia de una caja abierta en la sucursal actual.
    - Procesa la venta, incluyendo la validación del formulario de venta, el procesamiento de los detalles del pedido,
      la actualización del inventario y la generación de notificaciones.

    Validación:
    - Se requiere autenticación de usuario.
    - Se verifica la existencia de una caja abierta antes de permitir la venta.

    Métodos:
    - get: Maneja solicitudes HTTP GET para la vista del Punto de Venta.
    - get_context_data: Obtiene datos de contexto para renderizar la vista.
    - form_valid: Maneja la presentación del formulario cuando este es válido, realizando las siguientes acciones:

        - Obtiene la sucursal actual y verifica la existencia de una caja abierta.
        - Procesa la venta, incluyendo la validación del formulario de venta, el procesamiento de los detalles del pedido,
          la actualización del inventario y la generación de notificaciones.
        - Realiza validaciones específicas, como la selección de cliente antes de vender ciertos productos, la verificación
          del monto pagado en relación con el total de la venta y la aplicación de descuentos válidos.
        - Maneja mensajes de error y redirige según las validaciones.

        Returns:
        - HttpResponseRedirect: Redirección a la vista de detalles de la venta.

    - form_invalid: Maneja el caso en que el formulario presentado no es válido.

        Returns:
        - HttpResponse: Respuesta HTTP para el caso de formulario no válido.
    """

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """
        Maneja solicitudes HTTP GET para la vista del Punto de Venta.

        Returns:
        - HttpResponse: Respuesta HTTP para la solicitud.
        """
        # ... (implementación detallada del método)

    def get_context_data(self, **kwargs):
        """
        Obtiene datos de contexto para renderizar la vista.

        Returns:
        - dict: Diccionario con datos adicionales para el contexto.
        """
        # ... (implementación detallada del método)

    @transaction.atomic
    def form_valid(self, form):
        """
        Maneja la presentación del formulario cuando este es válido.

        Lógica:
        - Obtiene la sucursal actual y verifica la existencia de una caja abierta.
        - Procesa la venta, incluyendo la validación del formulario de venta, el procesamiento de los detalles del pedido,
          la actualización del inventario y la generación de notificaciones.
        - Realiza validaciones específicas, como la selección de cliente antes de vender ciertos productos, la verificación
          del monto pagado en relación con el total de la venta y la aplicación de descuentos válidos.
        - Maneja mensajes de error y redirige según las validaciones.

        Returns:
        - HttpResponseRedirect: Redirección a la vista de detalles de la venta.
        """
        # ... (implementación detallada del método)

        def form_invalid(self, form):
        """
        Maneja el caso en que el formulario presentado no es válido.

        Returns:
        - HttpResponse: Respuesta HTTP para el caso de formulario no válido.
        """
        # ... (implementación detallada del método)


################## PAYMENT METHOD ######################

**PaymentMethodCreateView:**

Vista para la creación de una nueva forma de pago.

Esta vista permite a los usuarios con los permisos adecuados agregar una nueva forma de pago al sistema. La forma de pago incluye campos como el nombre y el tipo de método. El usuario que realiza la creación se registra como el creador de la forma de pago.

- **Métodos:**
  - `form_valid(form):`
    - Maneja la presentación del formulario cuando este es válido.
    - Guarda la nueva forma de pago asignando el usuario actual como creador.
    - En caso de solicitud AJAX, devuelve una respuesta JSON con los detalles de la nueva forma de pago.
    - Si no es una solicitud AJAX, llama al método form_valid del padre para el comportamiento predeterminado.

  - `form_invalid(form):`
    - Maneja el caso en que el formulario presentado no es válido.
    - En caso de solicitud AJAX, devuelve una respuesta JSON con un mensaje de error.
    - Si no es una solicitud AJAX, imprime detalles del formulario no válido y llama al método form_invalid del padre.

**PaymentMethodView:**

Vista para listar todas las formas de pago disponibles.

Esta vista presenta una lista paginada de todas las formas de pago registradas en el sistema. Solo los usuarios autorizados pueden acceder a esta lista.

- **Métodos:**
  - `get_context_data(**kwargs):`
    - Obtiene datos de contexto para renderizar la vista.
    - Incluye el formulario de creación de formas de pago en el contexto.

---

**Funciones de Peticiones AJAX:**

Las siguientes funciones son vistas basadas en funciones que manejan peticiones AJAX para generar componentes específicos, como facturas y comprobantes de pago. Estas funciones proporcionan una salida HTML en lugar de renderizar vistas completas.

- `show_invoice(request, pk):`
  - Muestra una factura para una venta específica.
  - Se utiliza en solicitudes AJAX y devuelve un HTML formateado.

- `show_factura(request, pk):`
  - Muestra un comprobante de pago para una venta específica.
  - Se utiliza en solicitudes AJAX y devuelve un HTML formateado.

- `gen_factura(request, pk):`
  - Genera una factura para una venta específica basándose en la opción seleccionada.
  - Se utiliza en solicitudes POST y redirige a la vista detallada de la venta.

---

**Vistas de Ventas:**

Las siguientes vistas manejan la presentación y detalles de las ventas.

- `SalesListView:`
  - Lista todas las ventas en el sistema paginadas.
  - Muestra detalles como el número de factura, la sucursal, el descuento, etc.

- `SaleDetailView:`
  - Muestra detalles específicos de una venta, incluidos los productos vendidos y los detalles del servicio asociado.

################## GESTIÓN DE VENTAS ######################

**set_serviceOrder_onSale:**

Este método asocia una orden de servicio a una venta específica. La orden de servicio se genera utilizando la función `process_service_order`, que procesa los datos del formulario de orden de servicio y los asocia al cliente de la venta. Luego, se asigna la venta a esta orden de servicio y se guarda.

- **Parámetros:**
  - `request`: La solicitud HTTP recibida.
  - `pk`: La clave primaria de la venta a la que se asociará la orden de servicio.

- **Acciones:**
  - Obtiene la venta y el cliente asociado.
  - Procesa la orden de servicio.
  - Asigna la venta a la orden de servicio.
  - Guarda la orden de servicio.
  - Redirige a la vista detallada de la venta asociada.

**pay_missing_balance:**

Este método maneja el pago del saldo faltante de una venta. Verifica si la solicitud es de tipo POST y realiza las siguientes acciones:

- Obtiene la venta y la sucursal actual.
- Valida el formulario de tipo de método de pago (`TypePaymentMethodForm`).
- Crea un movimiento en la caja con la cantidad del saldo faltante de la venta.
- Registra el pago en la venta.
- Actualiza el estado y el saldo faltante de la venta.
- Actualiza objetivos para el usuario que realizó la venta.

En caso de éxito, muestra un mensaje de éxito y redirige a la vista detallada de la venta.

- **Parámetros:**
  - `request`: La solicitud HTTP recibida.
  - `pk`: La clave primaria de la venta para la cual se realizará el pago del saldo faltante.

- **Acciones:**
  - Obtiene la venta y la sucursal.
  - Valida el formulario de tipo de método de pago.
  - Crea un movimiento en la caja.
  - Registra el pago en la venta.
  - Actualiza el estado y el saldo faltante de la venta.
  - Actualiza objetivos para el usuario.
  - Muestra mensajes de éxito o error y redirige a la vista detallada de la venta.
