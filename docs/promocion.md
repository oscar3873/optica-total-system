2x1 : Para cualquier combo que se arme con esta promocion, se tomara en el valor de la venta al precio del mayor valor 
    - P1 = $500  +  P2 = $1000  --> combo a $1000
    - P1 = $100  +  P2 = $200  --> combo a $200 

-%50 en la 2da unidad (para cualquier combo)
    - P1 = $500  +  P2 = $1000  --> combo a $1250 ($1000 + $500/2)
    - P1 = $100  +  P2 = $200  --> combo a $250 ($200 + $100/2)

Descuento fijo % o $
    - P1 = $1000 - 30% --> valor de venta $700
    - P1 = $100 - $50 --> valor de venta $50 



logica del 2x1 y 50% off 
    (BACKEND):
    - Desde un producto inicial P1:
        -> acceder a la tabla Promotions (fila asociada a P1)
        -> De la tabla Promotions de ese P1 saber que otro producto está relacionado (P2)
        -> Verificar si P1 y P2 fueron seleccionados durante la venta para aplicar promocion
    
    (FRONTEND):
    - Por el momento se podria mandar una lista de tuplas donde cada una de ellas estariam los id del "combo":
        Ej.: { '2x1': [
                        (1,3), (2,4), (11, 13)
                ],
                '50%': [
                    (23, 55), (7, 6)
                ],
                'descuento': [12, 14, 16]
            }
        con ello corroborar si los productos seleccionados pertenecen a una de esas tuplas y buscar si "alguna tupla se completa" (si estan los 2 productos seleccionados para aplicar promocion)
        o sino deberia consultar si tiene descuento unitario (PENSARLO BIEN)






#################################### CREATE ####################################
class PromotionCreateView(CustomUserPassesTestMixin, FormView):
    """
    Vista para crear una nueva promoción.

    Lógica:
    - Se crea una nueva promoción a partir de los datos del formulario.
    - Se asigna la sucursal actual del usuario a la promoción.
    - Se guardan los productos asociados a la promoción.

    Validación:
    - Se verifica que el usuario tenga los permisos adecuados para crear una promoción.
    """

    def form_valid(self, form):
        """
        Método llamado cuando el formulario es válido. Crea y guarda la promoción en la base de datos.

        Parameters:
        - form: Instancia del formulario válido.

        Returns:
        - HttpResponseRedirect: Redirige a la página de inicio o a la URL especificada en success_url.
        """
        # ... (implementación detallada del método)


#################################### DETAILS ####################################
class PromotionDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para ver los detalles de una promoción.

    Lógica:
    - Se verifica que el usuario tenga permisos para ver la promoción.
    - Se obtienen los productos asociados a la promoción y se agregan al contexto.

    Validación:
    - Se verifica que el usuario tenga permisos adecuados para acceder a la vista detallada.
    """

    def get(self, request, *args, **kwargs):
        """
        Método llamado cuando se realiza una solicitud GET. Verifica los permisos del usuario para ver la promoción.

        Parameters:
        - request: Objeto de solicitud HTTP.
        - args: Argumentos adicionales.
        - kwargs: Argumentos de palabra clave adicionales.

        Returns:
        - super().get(): Retorna la respuesta generada por el método get de la clase padre.
        """
        # ... (implementación detallada del método)

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la vista.

        Returns:
        - dict: Diccionario con datos adicionales para el contexto.
        """
        # ... (implementación detallada del método)


#################################### UPDATE ####################################
class PromotionUpdateView(CustomUserPassesTestMixin, UpdateView):
    """
    Vista para actualizar una promoción existente.

    Lógica:
    - Se obtienen los productos relacionados con la promoción y se agregan al contexto.
    - Se actualiza la promoción y sus productos asociados en la base de datos.

    Validación:
    - Se verifica que el usuario tenga permisos adecuados para acceder a la vista de actualización.
    """

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la vista.

        Returns:
        - dict: Diccionario con datos adicionales para el contexto.
        """
        # ... (implementación detallada del método)

    def form_valid(self, form):
        """
        Método llamado cuando el formulario es válido. Actualiza la promoción en la base de datos.

        Parameters:
        - form: Instancia del formulario válido.

        Returns:
        - HttpResponseRedirect: Redirige a la página de detalles de la promoción actualizada.
        """
        # ... (implementación detallada del método)


#################################### LIST ####################################
class PromotionListView(LoginRequiredMixin, ListView):
    """
    Vista para listar las promociones disponibles.

    Lógica:
    - Se filtran las promociones por la sucursal actual del usuario.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la lista de promociones.
    """

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la vista.

        Returns:
        - dict: Diccionario con datos adicionales para el contexto.
        """
        # ... (implementación detallada del método)

    def get_queryset(self):
        """
        Retorna el conjunto de promociones filtradas por la sucursal actual del usuario.

        Returns:
        - QuerySet: Conjunto de promociones filtradas.
        """
        # ... (implementación detallada del método)


#################################### DELETE ####################################
class PromotionDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar una promoción existente.

    Lógica:
    - Se eliminan las relaciones de productos asociados a la promoción.
    - Se realiza una eliminación suave de la promoción.

    Validación:
    - Se verifica que el usuario tenga permisos adecuados para acceder a la vista de eliminación.
    """

    def form_valid(self, form):
        """
        Método llamado cuando se confirma la eliminación de la promoción. Elimina la promoción y sus relaciones.

        Returns:
        - HttpResponseRedirect: Redirige a la página de lista de promociones después de la eliminación.
        """
        # ... (implementación detallada del método)

