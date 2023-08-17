from django.db import models

from django.contrib.auth.models import BaseUserManager


class CustomerManager(BaseUserManager, models.Manager):
    """
    Manager para Clientes
    """
    def creat_customer(self, address, **extra_fields):
        customer = self.model(
            address = address,
            **extra_fields
        )
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