from django.db import models


# Create your models here.

class Genero(models.Model):
    id_genero = models.AutoField(db_column='idGenero', primary_key=True)
    genero    = models.CharField(max_length=20, blank=False, null=False)

    def _str_(self):
        return str(self.genero)


class Cliente(models.Model):
    rut            = models.CharField(primary_key=True, max_length=10)
    nombre         = models.CharField(max_length=20)
    apellido_M     = models.CharField(max_length=20)
    apellido_P     = models.CharField(max_length=20)
    id_genero      = models.ForeignKey('Genero',on_delete=models.CASCADE, db_column='id_Genero')
    telefono       = models.CharField(max_length=45)
    direccion      = models.CharField(max_length=50, blank=True, null=True)

    def _str_(self):
        return str(self.nombre)+ " " +str(self.apellido_P)
    
    class Meta:
        ordering = ['rut']


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')

class Carrito(models.Model):
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

