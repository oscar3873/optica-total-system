def form_in_out_insurances(form, customer, user):
        """
        PARA FORMULARIOS:
            Verifica el estado de las obras sociales despues del update.
            En caso de que se hayan deseleccionado alguna, debe ser quitada de la tabla intermedia
            En el caso de agregar otra, se relaciona el cliente con dicha obra social mediante la tabla intermedia.

        """
        selected_h_insurance = form.cleaned_data['h_insurance']
        existing_h_insurance = customer.customer_insurance.all()

        # Elimina relaciones existentes que ya no están seleccionadas
        for intermedia in existing_h_insurance:
            if intermedia.h_insurance not in selected_h_insurance:
                customer.customer_insurance.get(h_insurance=intermedia.h_insurance).delete()

        # Crea nuevas relaciones solo para características no existentes
        for h_insurance in selected_h_insurance:
            if h_insurance not in existing_h_insurance.values_list('h_insurance', flat=True):
                intermedia, created = customer.customer_insurance.get_or_create(h_insurance=h_insurance)
                if created:
                    intermedia.user_made = user
                    intermedia.save()

def obtener_clave_por_subcadena(diccionario, subcadena):
        for clave in diccionario.keys():
            if subcadena in clave:
                return clave
        return None