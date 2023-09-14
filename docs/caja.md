#Procesos vinculados a la caja


- **Abrir una caja**: Podremos abrir una caja registradora solo si en la sucursal del `user`
    * No hay una caja: Esto solo ocurrira al iniciar el sistema que sera la primera vez que se puede llegar a crear una caja o en su defecto si se llegara a eliminar todas las cajas (cosa que deberia pasar).

    * Hay cajas, pero estan cerradas: Tener siempre en cuenta que la caja tiene un booleano `is_close` que indica el estado de la caja, por lo que repetimos que la caja no se elimina, ademas mas adelante se vera que la caja tiene un detalle de caja (para realizar el arqueo), movimientos, entre otras cosas.
    si hay cajas pero ```is_close = True``` sera una condicion para que un `user` pueda abrir una caja.

    * Que existan monedas: Existe una tabla `Currency` donde podemos crear una divisa determinada y como existe una relacion entre `Currency` y `Cashregister` (Una divisa puede estar presente en muchas cajas registradoras) es necesario tener creado esto y sera una condicion de apertura de la caja.


- **Listar una caja**: Existiran algunas condiciones para listar una caja en determinada sucursal
   * Que existan cajas que listar en la sucursal
   * Que pertenezca a la sucursal correspondiente
   * Solo podemos listar una caja por lo que no podremos tener  ```is_close = False``` en mas de una caja en simultaneo
Deberemos hacer cumplir esto con el fin de que no se pueda tener mas de una instancia en condicion de ```is_close = False``` ya que es muy sencillo romper esto por medio del administrador


- **Cerrar una caja**: Para poder cerrar una caja registradora
   * Primero debe existir una caja que cerrar
   * El proceso de cierre caja consiste en realizar un arqueo de caja mediante un modelo llamado `CashRegisterDetail` el cual a su vez tiene una relacion con `TypeMethodPayment` el cual detalla metodos como `Efectivo`, `Tarjeta de Credito`, `Tarjeta de Debito`, `Transferencia` en este proceso de arqueo se considera un balance final en `CashRegister` como balance de sistema que no distingue entre los `TypeMethodPayment`. Ahora bien, en `CashRegisterDetail` tendremos algunos campos como `type_method` que nos indica que tipos de metodos son (efectivo, tarjeta de credito, etc.) `registered_amount` el cual es el balance final considerando el tipo de metodo, `counted_amount` es el balance que da la caja fisica teniendo en cuenta el tipo de metodo y `difference` el cual es la discrepancia que existe entre lo que dice el sistema y lo que arroja el conteo de la caja fisica. Claramente esto se realiza por cada uno de los distintos tipos de metodos que tengamos (efectivo, transferencia, etc.). Una vez se completo el proceso de arqueo podemos cerrar la caja la cual consiste basicamente en cambiar el valor del booleano ```is_close = False``` a ```is_close = True``` y al hacer el guardado de eso se relaciona la caja actual de `CashRegister` con los detalles de arqueo en `CashRegisterDetail`.