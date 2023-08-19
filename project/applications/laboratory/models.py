from django.db import models

from applications.employes.models import Employee
# Create your models here.
class Correction(models.Model):
    esferic = models.CharField(max_length=20, null=True, blank=True)
    cilindric = models.CharField(max_length=20, null=True, blank=True)
    other = models.CharField(max_length=10, null=True, blank=True)

class Eye_left(Correction):
    pass
class Eye_right(Correction):
    pass
class Distance_far(Eye_left, Eye_right):
    pass
class Distance_close(Eye_left, Eye_right):
    pass
class Laboratory(Distance_far, Distance_close):
    detail = models.TextField(null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)