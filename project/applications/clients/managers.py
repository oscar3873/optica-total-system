from django.db import models

from django.contrib.auth.models import BaseUserManager


class CustomerManager(BaseUserManager, models.Manager):
    """
    Manager para Clientes
    """
    def create_customer(self, **data):
        customer = self.model(**data)
        customer.save()
        return customer

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
    

class MaterialManager(BaseUserManager, models.Manager):

    def cerate_material(self, policarbonato, organic, mineral, m_r8, user_made, **extra_fields):
        material = self.model(
            policarbonato = policarbonato,
            organic =organic,
            mineral = mineral,
            m_r8 = m_r8,
            user_made = user_made
            **extra_fields
        )
        mineral.save()
        return material
    
    def create_by_form(self, form, user_made):
        material = self.cerate_material(
            policarbonato = form.cleaned_data['policarbonato'],
            organic = form.cleaned_data['organic'],
            mineral = form.cleaned_data['mineral'],
            m_r8 = form.cleaned_data['m_r8'],
            user_made = user_made
        )
        return material