from django.db import models
from oreore_project import settings

class Prescription(models.Model):
    ownUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='own_user')
    prescriptionName = models.CharField(max_length=25)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prescriptionName

