from django.db import models
from oreore_project import settings
from prescription_manage.models import *

class Disease(models.Model):
    kcdCode = models.CharField(max_length=8)
    diesName = models.CharField(max_length=255)
    rgstrDate = models.DateTimeField(auto_now_add=True)

    linkPrescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    def __str__(self):
        return self.diesName