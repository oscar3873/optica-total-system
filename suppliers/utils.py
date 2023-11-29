from suppliers.models import Cbu

def delete_banks_not_assoc():
    banks = Cbu.objects.filter(suppliers=None)
    for bank in banks:
        bank.delete()