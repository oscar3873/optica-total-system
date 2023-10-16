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
