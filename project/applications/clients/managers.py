from typing import Any
from django.db import models

from django.contrib.auth.models import BaseUserManager

from applications.clients.models import Customer_HealthInsurance
from applications.sales.models import Sale


class CustomerManager(BaseUserManager, models.Manager):
    """
    Manager para Clientes
    """
    def creat_customer(self, person, address, **extra_fields):
        customer = self.model(
            person = person,
            address = address,
            **extra_fields
        )
        customer.save()
        return customer

    def update_phone_number(self, customer, phone_number):
        customer.person.phone_number = phone_number
        customer.save()
        
    def update_address(self, customer, address):
        customer.address = address
        customer.save()

    def history(self, customer):
        history = customer.medicalhistory.order_by('created_at')
        return history

    def all_insurance(self, customer):
        h_insurance = Customer_HealthInsurance.objects.filter(customer=customer).order_by('h_insurance')
        return h_insurance
    
    def all_buy(self, customer):
        buy = Sale.objects.filter(customer=customer).order_by('created_at')
        return buy