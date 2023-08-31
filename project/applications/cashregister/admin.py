from django.contrib import admin
from .models import Currency, CashRegister, PaymentMethod, Payment, Transaction, Movement, TransactionType, TypeMethodePayment

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    pass


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    pass

@admin.register(TypeMethodePayment)
class TypeMethodePayment(admin.ModelAdmin):
    pass
