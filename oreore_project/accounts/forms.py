from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('uid', 'age', 'sex', 'name')
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('uid', 'password', 'name','age','sex',
                  'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['uid', 'password', 'name', 'age', 'sex']
        widgets = {
            'uid': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # TODO: 여기 textinput바꿔야함
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'uid': '아이디',
            'password': '패스워드',
            'name': '이름',
            'age': '나이',
            'sex': '성별',
        }
    # 글자수 제한
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__( *args, **kwargs)
        self.fields['uid'].widget.attrs['maxlength'] = 15

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['uid', 'password']
        widgets = {
            'uid': forms.TextInput(attrs={'class': 'form-control'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'uid': 'ID',
            'password': 'PW',
        }
