from django.db import models
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel

class EyeCorrection(SoftDeletionModel, TimestampsModel):
    esferic = models.CharField(max_length=20, null=True, blank=True)
    cilindric = models.CharField(max_length=20, null=True, blank=True)
    eje = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        abstract = True

class Left_eye(EyeCorrection, SoftDeletionModel, TimestampsModel):
    distance = models.CharField(max_length=20, null=True, blank=True)

class Right_eye(EyeCorrection, SoftDeletionModel, TimestampsModel):
    distance = models.CharField(max_length=20, null=True, blank=True)

class Laboratory(SoftDeletionModel, TimestampsModel):
    left_eye = models.ForeignKey(Left_eye, on_delete=models.CASCADE, null=True, blank=True)
    right_eye = models.ForeignKey(Right_eye, on_delete=models.CASCADE, null=True, blank=True)