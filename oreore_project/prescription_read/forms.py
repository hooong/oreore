from django import forms
from .models import *

class Prescription_imgForm(forms.ModelForm):
    class Meta:
        model = Prescription_img
        fields = ['pre_img']

        labels = {
            'pre_img': '처방전'
        }