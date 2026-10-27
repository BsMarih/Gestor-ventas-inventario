from django import forms

class CreateElementForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=255)
    description = forms.CharField(label="Descripción", widget=forms.Textarea)
    price = forms.DecimalField(label="Precio", max_digits=10, decimal_places=2)
    quantity = forms.IntegerField(label="Cantidad")
    min_quantity = forms.IntegerField(label="Cantidad Mínima")
    distributor = forms.CharField(label="Distribuidor", max_length=255, required=False)
    prod_website = forms.URLField(label="Sitio Web del Producto", required=False)
    category = forms.CharField(label="Categoría", max_length=255)
    type = forms.CharField(label="Tipo", max_length=255)

class UserForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)