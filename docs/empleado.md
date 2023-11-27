#################################### CREATE ####################################
class EmployeeCreateView(CustomUserPassesTestMixin, FormView):
    """
    Vista para la creación de nuevos empleados.

    Lógica:
    - Se crea un nuevo empleado junto con un nuevo usuario.
    - El usuario se crea con la información proporcionada en el formulario.
    - El usuario se asocia con una sucursal y se asigna como empleado.

    Validación:
    - Se verifica que el usuario tenga los permisos adecuados para crear un empleado.
    """

    def form_valid(self, form):
        """
        Método llamado cuando el formulario es válido. Crea y guarda el nuevo empleado y usuario en la base de datos.

        Parameters:
        - form: Instancia del formulario válido.

        Returns:
        - HttpResponseRedirect: Redirige a la página de lista de empleados después de la creación.
        """
        # ... (implementación detallada del método)

    def form_invalid(self, form):
        """
        Método llamado cuando el formulario es inválido.

        Returns:
        - super().form_invalid(): Llama al método form_invalid de la clase padre.
        """
        # ... (implementación detallada del método)


#################################### UPDATE ####################################
class EmployeeUpdateView(UpdateView):
    """
    Vista para la actualización de datos de un empleado existente.

    Lógica:
    - Se actualizan los datos del usuario asociado al empleado con la información proporcionada en el formulario.

    Validación:
    - Se verifica que el formulario sea válido antes de realizar la actualización.
    """

    def form_valid(self, form):
        """
        Método llamado cuando el formulario es válido. Actualiza los datos del empleado y usuario en la base de datos.

        Parameters:
        - form: Instancia del formulario válido.

        Returns:
        - HttpResponseRedirect: Redirige a la página de lista de empleados después de la actualización.
        """
        # ... (implementación detallada del método)

    def form_invalid(self, form):
        """
        Método llamado cuando el formulario es inválido.

        Returns:
        - super().form_invalid(): Llama al método form_invalid de la clase padre.
        """
        # ... (implementación detallada del método)


############## UNICA VIEW DISPONIBLE PARA EL USO #############
# Perfil de empleado
class EmployeeProfileView(LoginRequiredMixin, DetailView):
    """
    Vista para visualizar el perfil de un empleado.

    Lógica:
    - Se muestra el perfil del empleado, incluyendo los objetivos asociados y objetivos de la sucursal.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder al perfil del empleado.
    """

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la vista.

        Returns:
        - dict: Diccionario con datos adicionales para el contexto.
        """
        # ... (implementación detallada del método)

    def get_object(self, queryset=None): 
        """
        Obtén el valor del parámetro 'pk' de la URL, este parámetro debe estar relacionado con la tabla users_employee.

        Returns:
        - Employee: Instancia del empleado asociado a la 'pk' proporcionada.
        """
        # ... (implementación detallada del método)


################################## LISTING  ##################################
class EmployeeListView(LoginRequiredMixin, ListView):
    """
    Vista para listar los empleados disponibles.

    Lógica:
    - Se filtran los empleados por la sucursal actual del usuario.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la lista de empleados.
    """

    def get_queryset(self):
        """
        Retorna el conjunto de empleados filtrados por la sucursal actual del usuario.

        Returns:
        - QuerySet: Conjunto de empleados filtrados.
        """
        # ... (implementación detallada del método)

    def get_context_data(self, **kwargs):
        """
        Añade datos adicionales al contexto de la vista.

        Returns:
        - dict: Diccionario con datos adicionales para el contexto.
        """
        # ... (implementación detallada del método)


########################### DELETE ####################################

class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar un empleado existente.

    Lógica:
    - Se desactiva el usuario asociado al empleado, realizando una eliminación suave.
    - Se elimina el registro del empleado.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados para acceder a la vista de eliminación.
    """

    def form_valid(self,form):
        """
        Método llamado cuando se confirma la eliminación del empleado.

        Returns:
        - HttpResponseRedirect: Redirige a la página de lista de empleados después de la eliminación
