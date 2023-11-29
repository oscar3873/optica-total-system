################################ CATEGORY CREATE VIEW ################################
class CategoryCreateView(CustomUserPassesTestMixin, FormView):
    """
    Vista para crear una nueva categoría de producto.

    Lógica:
    - Almacena la nueva categoría en la base de datos.
    - Maneja solicitudes AJAX para actualizaciones en tiempo real.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.
    - Comprueba si la solicitud es AJAX para respuestas diferenciadas.

    Métodos Relevantes:
    - form_valid: Almacena la nueva categoría y maneja solicitudes AJAX.
    - form_invalid: Maneja la respuesta en caso de datos de formulario no válidos.

################################ BRAND CREATE VIEW ################################
class BrandCreateView(LoginRequiredMixin, FormView):
    """
    Vista para crear una nueva marca de producto.

    Lógica:
    - Almacena la nueva marca en la base de datos.
    - Maneja solicitudes AJAX para actualizaciones en tiempo real.

    Validación:
    - Se verifica que el usuario esté autenticado.
    - Comprueba si la solicitud es AJAX para respuestas diferenciadas.

    Métodos Relevantes:
    - form_valid: Almacena la nueva marca y maneja solicitudes AJAX.
    - form_invalid: Maneja la respuesta en caso de datos de formulario no válidos.

################################ FEATURE CREATE VIEW ################################
class FeatureCreateView(CustomUserPassesTestMixin, FormView):
    """
    Vista para crear una nueva característica para el producto.

    Lógica:
    - Almacena la nueva característica en la base de datos y la asocia con productos seleccionados.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - form_valid: Almacena la nueva característica y la asocia con productos seleccionados.

############################ FEATURE FULL CREATE VIEW ############################
class FeatureFullCreateView(FormView):
    """
    Vista para crear una nueva característica y su tipo asociado.

    Lógica:
    - Valida la existencia de la característica y su tipo.
    - Maneja solicitudes AJAX para actualizaciones en tiempo real.

    Validación:
    - Comprueba si la solicitud es AJAX para respuestas diferenciadas.

    Métodos Relevantes:
    - form_valid: Valida y crea la nueva característica y tipo, maneja solicitudes AJAX.

########################### FEATURE UNIT CREATE VIEW ##############################
class FeatureUnitCreateView(FormView):
    """
    Vista para añadir una característica a un tipo existente.

    Lógica:
    - Valida y crea la nueva característica asociada a un tipo.
    - Maneja solicitudes AJAX para actualizaciones en tiempo real.

    Validación:
    - Comprueba si la solicitud es AJAX para respuestas diferenciadas.

    Métodos Relevantes:
    - form_valid: Valida y crea la nueva característica asociada a un tipo, maneja solicitudes AJAX.

############################ FEATURE TYPE CREATE VIEW ##############################
class FeatureTypeCreateView(CustomUserPassesTestMixin, FormView):
    """
    Vista para crear un nuevo tipo de característica para el producto.

    Lógica:
    - Almacena el nuevo tipo en la base de datos.
    - Maneja solicitudes AJAX para actualizaciones en tiempo real.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.
    - Comprueba si la solicitud es AJAX para respuestas diferenciadas.

    Métodos Relevantes:
    - form_valid: Almacena el nuevo tipo y maneja solicitudes AJAX.
    - form_invalid: Maneja la respuesta en caso de datos de formulario no válidos.

########################## PRODUCT CREATE VIEW (WIZARD) ###########################
class ProductCreateView(CustomUserPassesTestMixin, FormView):
    """
    Vista para crear un nuevo producto con características.

    Lógica:
    - Almacena el nuevo producto y sus características asociadas en la base de datos.
    - Maneja solicitudes AJAX para actualizaciones en tiempo real.
    - Determina la URL de redirección según la ruta de origen.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.
    - Comprueba si la solicitud es AJAX para respuestas diferenciadas.

    Métodos Relevantes:
    - form_valid: Almacena el nuevo producto y maneja solicitudes AJAX.
    - form_invalid: Maneja la respuesta en caso de datos de formulario no válidos.

########################## PRODUCT UPDATE VIEW (WIZARD) ###########################
class ProductUpdateView(CustomUserPassesTestMixin, UpdateView):
    """
    Vista para actualizar un producto existente con características.

    Lógica:
    - Actualiza el producto y sus características asociadas en la base de datos.
    - Maneja solicitudes AJAX para actualizaciones en tiempo real.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - form_valid: Actualiza el producto y maneja solicitudes AJAX.

######################### CATEGORY UPDATE VIEW ##########################
class CategoryUpdateView(CustomUserPassesTestMixin, UpdateView):
    """
    Vista para actualizar una categoría existente.

    Lógica:
    - Actualiza la categoría en la base de datos.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - form_valid: Actualiza la categoría.

########################### BRAND UPDATE VIEW ###########################
class BrandUpdateView(CustomUserPassesTestMixin, UpdateView):
    """
    Vista para actualizar una marca existente.

    Lógica:
    - Actualiza la marca en la base de datos.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - form_valid: Actualiza la marca.

######################### FEATURE UPDATE VIEW ##########################
class FeatureUpdateView(CustomUserPassesTestMixin, UpdateView):
    """
    Vista para actualizar una característica existente.

    Lógica:
    - Actualiza la característica en la base de datos.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - form_valid: Actualiza la característica.

######################## FEATURE TYPE UPDATE VIEW ##########################
class FeatureTypeUpdateView(CustomUserPassesTestMixin, UpdateView):
    """
    Vista para actualizar un tipo de característica existente.

    Lógica:
    - Actualiza el tipo de característica en la base de datos.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - form_valid: Actualiza el tipo de característica.

######################## PRODUCT LIST VIEW ##########################
class ProductListView(LoginRequiredMixin, ListView):
    """
    Vista para listar productos disponibles.

    Lógica:
    - Filtra los productos por la sucursal actual del usuario.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - get_queryset: Filtra los productos por la sucursal actual del usuario.
    """

######################## BRAND LIST VIEW ##########################
class BrandListView(LoginRequiredMixin, ListView):
    """
    Vista para listar marcas disponibles.

    Lógica:
    - Filtra las marcas que no han sido eliminadas suavemente.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - get_queryset: Filtra las marcas que no han sido eliminadas suavemente.
    """


######################## CATEGORY LIST VIEW ##########################
class CategoryListView(LoginRequiredMixin, ListView):
    """
    Vista para listar categorías de productos.

    Lógica:
    - Filtra las categorías que no han sido eliminadas suavemente.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - get_queryset: Filtra las categorías que no han sido eliminadas suavemente.
    - get_context_data: Agrega el nombre de las columnas de la tabla al contexto.
    """

######################## FEATURE TYPE LIST VIEW ##########################
class FeatureTypeListView(LoginRequiredMixin, ListView):
    """
    Vista para listar tipos de características de productos.

    Lógica:
    - Filtra los tipos de características que no han sido eliminados suavemente.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - get_queryset: Filtra los tipos de características que no han sido eliminados suavemente.
    """

######################## FEATURE LIST VIEW ##########################
class FeatureListView(LoginRequiredMixin, ListView):
    """
    Vista para listar características de productos.

    Lógica:
    - Filtra las características que no han sido eliminadas suavemente.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - get_queryset: Filtra las características que no han sido eliminadas suavemente.
    """

#################### PRODUCT DETAIL VIEW ######################
class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para ver detalles de un producto.

    Lógica:
    - Verifica que el usuario tenga permisos para ver el producto basado en la sucursal.
    - Obtiene y muestra las características del producto.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - get: Realiza la verificación de permisos antes de mostrar el detalle del producto.
    - get_context_data: Agrega las características y el proveedor al contexto.
    """

#################### CATEGORY DETAIL VIEW ######################
class CategoryDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para ver detalles de una categoría.

    Lógica:
    - Obtiene y muestra los productos asociados a la categoría.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - get_context_data: Agrega los productos relacionados al contexto.
    """

#################### BRAND DETAIL VIEW ######################
class BrandDetailView(LoginRequiredMixin, DetailView):
    """
    Vista para ver detalles de una marca.

    Lógica:
    - Obtiene y muestra los productos asociados a la marca.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - get_context_data: Agrega los productos relacionados al contexto.
    """

########################### DELETE VIEWS ###############################
# FALTA COMPLETAR LA LÓGICA PARA EL BORRADO SUAVE DE LAS INSTANCIAS RELACIONADAS
# ¿QUÉ PASA SI BORRO UNA FEATURE QUE YA ESTÁ RELACIONADA PREVIAMENTE CON ALGÚN PRODUCTO? (PROTECTED NO DEJARÁ QUE BORRE)

class CategoryDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar una categoría de productos.

    Lógica:
    - Permite el borrado suave de la categoría.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Atributos Relevantes:
    - model: Modelo de la categoría.
    - template_name: Plantilla para la vista.
    - success_url: URL a redirigir después de eliminar la categoría.
    """

class BrandDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar una marca de productos.

    Lógica:
    - Permite el borrado suave de la marca.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Atributos Relevantes:
    - model: Modelo de la marca.
    - template_name: Plantilla para la vista.
    - success_url: URL a redirigir después de eliminar la marca.
    """

class ProductDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar un producto.

    Lógica:
    - Permite el borrado suave del producto.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Atributos Relevantes:
    - model: Modelo del producto.
    - template_name: Plantilla para la vista.
    - success_url: URL a redirigir después de eliminar el producto.
    """

class FeatureDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar una característica de producto.

    Lógica:
    - Falta completar la lógica para el borrado suave de las instancias relacionadas.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Atributos Relevantes:
    - model: Modelo de la característica de producto.
    - template_name: Plantilla para la vista.
    - success_url: URL a redirigir después de eliminar la característica de producto.
    """

class FeatureTypeDeleteView(CustomUserPassesTestMixin, DeleteView):
    """
    Vista para eliminar un tipo de característica de producto.

    Lógica:
    - Falta completar la lógica para el borrado suave de las instancias relacionadas.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Atributos Relevantes:
    - model: Modelo del tipo de característica de producto.
    - template_name: Plantilla para la vista.
    - success_url: URL a redirigir después de eliminar el tipo de característica de producto.
    """

###################### SEARCH VIEW #########################
class ProductSearchView(ListView):
    """
    Buscador de productos para el Punto de Venta (PoS).
    ¡¡SOLO PARA PETICIONES FETCH!!

    Métodos Relevantes:
    - get_queryset: Realiza una búsqueda insensible a mayúsculas/minúsculas y que contenga la palabra en los campos 'name' y 'barcode'.
    - get: Retorna una respuesta JSON con los productos que coinciden con la búsqueda.
    """

#################### UPDATE PRICE VIEW ######################
class UpdatePriceView(CustomUserPassesTestMixin, FormView):
    """
    Vista para actualizar los precios de productos.

    Lógica:
    - Calcula y actualiza los precios de productos basados en marcas, categorías y un porcentaje.

    Validación:
    - Se verifica que el usuario esté autenticado y tenga permisos adecuados.

    Métodos Relevantes:
    - form_valid: Realiza el cálculo y actualización de precios.
    - form_invalid: Muestra errores en caso de que el formulario no sea válido.
    """

#################### SEARCH CATEGORIES OR BRANDS ######################
@require_GET
def search_categories_or_brands(request):
    """
    Vista para buscar categorías o marcas.

    Métodos Relevantes:
    - get: Retorna una respuesta JSON con los resultados de búsqueda de categorías y marcas.
    """

#################### EXPORT PRODUCTS LIST TO EXCEL ######################
def export_products_list_to_excel(request):
    """
    Vista para exportar la lista de productos a un archivo Excel.

    Métodos Relevantes:
    - get_products_branch: Obtiene la lista de productos de la sucursal actual.
    - obtener_nombres_de_campos: Obtiene los nombres de los campos del modelo Product.
    - get: Genera un archivo Excel con la lista de productos y lo devuelve como respuesta HTTP.
    """

################ SEARCH PRODUCTS AJAX ######################
def ajax_search_products(request):
    """
    Vista para buscar productos de forma asíncrona.

    Métodos Relevantes:
    - get_products_branch: Obtiene la lista de productos de la sucursal actual.
    - get: Retorna una respuesta JSON con los productos que coinciden con la búsqueda.
    """

@require_http_methods(["GET"])
def obtener_stock(request):
    """
    Vista para obtener el stock de un producto de forma asíncrona.

    Métodos Relevantes:
    - get: Retorna una respuesta JSON con el stock del producto.
    """
