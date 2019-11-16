from django.db import models
from prescription_manage.models import *

class Medicine(models.Model):
    mediName = models.CharField(max_length=255)
    insuranceCode = models.CharField(max_length=15)
    img_url = models.CharField(max_length=500, default='')
    entp = models.CharField(max_length=500, default='')
    class_name = models.CharField(max_length=500, default='')
    dosage = models.CharField(max_length=500, default='')
    caution = models.CharField(max_length=500, default='')
    rgstrDate = models.DateTimeField(auto_now_add=True)
    

    linkPrescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='related_disease')

    def __str__(self):
        return self.mediName