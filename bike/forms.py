# forms.py
from django import forms
from .models import Producto, Cliente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'imagen', 'precio', 'stock', 'categoria']

class RegistroClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
