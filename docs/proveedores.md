################## GESTIÓN DE PROVEEDORES ######################

**SupplierCreateView:**

Esta vista permite la creación de un nuevo proveedor. Incluye un formulario (`SupplierForm`) para recopilar información sobre el proveedor, como nombre, dirección, etc. También permite asociar marcas y cuentas bancarias al proveedor.

- **Parámetros:**
  - `form_valid`: Maneja la presentación del formulario cuando es válido.
  - `get_context_data`: Obtiene datos de contexto para la renderización de la vista.

**SupplierUpdateView:**

Esta vista permite la actualización de la información de un proveedor existente. Permite modificar los datos del proveedor, las marcas asociadas y las cuentas bancarias asociadas.

- **Parámetros:**
  - `form_valid`: Maneja la presentación del formulario cuando es válido.
  - `get_context_data`: Obtiene datos de contexto para la renderización de la vista.

**BankUpdateView:**

Esta vista permite la actualización de la información de una cuenta bancaria asociada a un proveedor. Utiliza el formulario `CBUForm` para recopilar información sobre la cuenta bancaria.

- **Parámetros:**
  - `get_success_url`: Obtiene la URL de redirección después de una actualización exitosa.

**SuppliersListView:**

Esta vista muestra una lista de proveedores registrados. Utiliza una plantilla para mostrar la información de los proveedores y proporciona un contexto con los campos de la tabla.

- **Parámetros:**
  - `get_context_data`: Obtiene datos de contexto para la renderización de la vista.

**SupplierDetailView:**

Esta vista muestra detalles sobre un proveedor específico. Incluye información sobre las marcas y cuentas bancarias asociadas al proveedor.

- **Parámetros:**
  - `get_context_data`: Obtiene datos de contexto para la renderización de la vista.

**SupplierDeleteView:**

Esta vista maneja la eliminación de un proveedor. Realiza una eliminación suave, marcando el proveedor como eliminado.

- **Parámetros:**
  - `delete`: Realiza la eliminación suave.

**Funciones AJAX:**

Estas funciones manejan operaciones asíncronas para la creación, búsqueda y eliminación de cuentas bancarias asociadas a proveedores.

- **Funciones:**
  - `set_bank_supplier`: Crea una nueva cuenta bancaria asociada a un proveedor.
  - `ajax_new_bank`: Crea una nueva cuenta bancaria.
  - `ajax_search_brands`: Realiza una búsqueda de marcas.
  - `ajax_delete_bank`: Elimina una cuenta bancaria asociada a un proveedor.
