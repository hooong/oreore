from django.db import models
from oreore_project import settings

class Disease(models.Model):
    ownUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='own_user')
    kcdCode = models.CharField(max_length=8)
    diesName = models.CharField(max_length=255)
    rgstrDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.diesName