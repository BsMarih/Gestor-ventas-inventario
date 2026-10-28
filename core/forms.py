from django import forms
from .models import Element

class CreateElementForm(forms.ModelForm):

    category = forms.CharField(max_length=255, strip=True)
    type = forms.CharField(max_length=255, strip=True)

    class Meta:
        model = Element
        fields = [
            'name',
            'description',
            'content',
            'price',
            'quantity',
            'min_quantity',
            'available',
            'distributor',
            'prod_website',
        ]

class UserForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)