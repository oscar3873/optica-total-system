from django.urls import reverse
from applications.core.managers import BaseManager

class CustomerManager(BaseManager):
    """
    Manager para Clientes
    """
    def all(self):
        return self.filter(deleted_at=None)

    def history(self, customer):
        history = customer.serviceorders.all().order_by('-created_at')
        return history

    def all_insurance(self, customer):
        health_insurances = customer.customer_insurance.order_by('h_insurance')
        return health_insurances
    
    def all_buy(self, customer):
        buy = customer.sales.all().order_by('created_at')
        return buy
        
    def get_absolute_url(self):
        return reverse('clients_app:detail', kwargs={'pk': self.pk})

class ServiceOrderManager(BaseManager):
    """
    Manager para el Pedido de laboratorio (Orden de Servicio)
    """
    def all(self):
        return self.filter(deleted_at=None)
    
    def create_lab(self, user_made,
                    form, correction_form, material_form, color_form,
                    cristal_form, tratamiento_form, pupilar_form,
                    customer):
        
        correction = correction_form.save(commit=False)
        correction.user_made = user_made
        correction.save()

        material = material_form.save(commit=False)
        material.user_made = user_made
        material.save()

        color = color_form.save(commit=False)
        color.user_made = user_made
        color.save()

        cristal = cristal_form.save(commit=False)
        cristal.user_made = user_made
        cristal.save()

        tratamiento = tratamiento_form.save(commit=False)
        tratamiento.user_made = user_made
        tratamiento.save()

        pupilar = pupilar_form.save(commit=False)
        pupilar.user_made = user_made
        pupilar.save()

        service_order = self.model(
            customer = customer,
            correction = correction,
            material = material,
            type_cristal = cristal,
            color = color,
            tratamient = tratamiento,
            interpupillary = pupilar,
            diagnostic = form.cleaned_data['diagnostic'],
            armazon = form.cleaned_data['armazon'],
            observations = form.cleaned_data['observations'],
            user_made = user_made,
        )
        # Set any other fields of the service_order as needed
        service_order.save()

        return service_order