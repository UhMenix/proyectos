from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    idGenero = models.AutoField(primary_key=True)
    nombre_genero = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre_genero

class Cliente(models.Model):
    rut = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=20)
    apellido_M = models.CharField(max_length=20)
    apellido_P = models.CharField(max_length=20)
    telefono = models.CharField(max_length=45)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
class Carrito(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, default=timezone.now)
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

    def __str__(self):
        return f"Carrito de {self.cliente.user.username}"

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} en el carrito de {self.carrito.cliente.user.username}"

class Boleta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=50, default='recibido')

    def __str__(self):
        return f'Boleta #{self.id} - {self.cliente.user.username}'

class DetalleCompra(models.Model):
    boleta = models.ForeignKey(Boleta, related_name='detalles_compra', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'
