from django.db import models
from oreore_project import settings

# 처방전 이미지 모델
class Prescription_img(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescription_img')
    pre_img = models.ImageField(upload_to="prescription_img")
   