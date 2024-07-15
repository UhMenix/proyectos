from django.contrib import admin
from .models import Producto, Boleta, DetalleCompra, Cliente, Carrito, CarritoProducto, Genero, Categoria

admin.site.register(Producto)
admin.site.register(Boleta)
admin.site.register(DetalleCompra)
admin.site.register(Cliente)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
admin.site.register(Genero)
admin.site.register(Categoria)