from django.db import models
from disease_manage.models import *

class Medicine(models.Model):
    mediName = models.CharField(max_length=255)
    insuranceCode = models.CharField(max_length=15)
    rgstrDate = models.DateTimeField(auto_now_add=True)

    relatedDisease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='related_disease')

    def __str__(self):
        return self.mediName