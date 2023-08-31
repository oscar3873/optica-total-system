from django.db import models

from django.contrib.auth.models import BaseUserManager


class CustomerManager(BaseUserManager, models.Manager):
    """
    Manager para Clientes
    """
    def update_phone_number(self, customer, phone_number):
        customer.phone_number = phone_number
        customer.save()
        
    def update_address(self, customer, address):
        customer.address = address
        customer.save()

    def history(self, customer):
        history = customer.medicalhistory.order_by('created_at')
        return history

    def all_insurance(self, customer):
        health_insurances = customer.customer_insurance.all().order_by('h_insurance')
        return health_insurances
    
    def all_buy(self, customer):
        buy = customer.sales.all().order_by('created_at')
        return buy
    

class LabManager(BaseUserManager, models.Manager):

    def create_or_update_calibration_order(self, user_made,
                    form, correction_form, material_form, color_form,
                    cristal_form, tratamiento_form, pupilar_form):
        
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

        calibration_order = self.model(
            is_done = form.cleaned_data['is_done'],
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
        # Set any other fields of the calibration_order as needed
        calibration_order.save()

        return calibration_order
