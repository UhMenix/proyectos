from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.utils import IntegrityError
from django.views.generic import ListView, CreateView
from rest_framework import generics
from .models import Producto, Boleta, DetalleCompra, Cliente, Carrito, CarritoProducto, Genero
from .forms import ProductoForm
from .serializers import ProductoSerializer

# Vista para la página de inicio
class IndexView(View):
    def get(self, request):
        return render(request, 'bike/index.html')

# Vista para la página "Acerca de"
class AboutView(View):
    def get(self, request):
        return render(request, 'bike/about.html')

# Vista para la página de contacto
class ContactView(View):
    def get(self, request):
        return render(request, 'bike/contact.html')

# Vista para mostrar la lista de productos (bikes)
class BikesView(ListView):
    model = Producto
    template_name = 'bike/bikes.html'
    context_object_name = 'productos'
    paginate_by = 12  # 12 productos por página

# Vista para la API
class ApiView(View):
    def get(self, request):
        return render(request, 'bike/api.html')

# Vista para listar todos los clientes (requiere permisos de administrador)
class ClientesView(ListView):
    model = Cliente
    template_name = 'bike/clientes.html'
    context_object_name = 'clientes'

# Vista para el registro de usuarios
class RegisterView(CreateView):
    template_name = 'bike/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')  

    def form_valid(self, form):
        user = form.save()

        # Obtener el género por defecto o el seleccionado por el usuario
        genero_id = self.request.POST.get('genero_id', 1)  

        try:
            genero = Genero.objects.get(pk=genero_id)
        except Genero.DoesNotExist:
            messages.error(self.request, 'El género seleccionado no es válido.')
            return super().form_invalid(form)

        try:
            cliente = Cliente.objects.create(
                user=user,
                rut=user.username,
                nombre='',
                apellido_M='',
                apellido_P='',
                telefono='',
                direccion='',
                genero=genero  
            )
            login(self.request, user)  
            messages.success(self.request, 'Registro exitoso. Bienvenido!')
            return super().form_valid(form)
        except Exception as e: 
            messages.error(self.request, f'Hubo un problema con el registro: {e}')
            return super().form_invalid(form)

# Vista para listar y crear productos
class ListaProductosView(ListView):
    """
    Vista para listar y crear productos.
    """
    model = Producto
    template_name = 'bike/lista_productos.html'
    context_object_name = 'productos'

class CrearProductoView(View):
    """
    Vista para crear un nuevo producto.
    """
    def get(self, request):
        form = ProductoForm()
        return render(request, 'bike/crear_producto.html', {'form': form})

    def post(self, request):
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
        return render(request, 'bike/crear_producto.html', {'form': form})

class VerProductoView(View):
    """
    Vista para ver detalles de un producto específico.
    """
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        return render(request, 'bike/ver_producto.html', {'producto': producto})

class ActualizarProductoView(View):
    """
    Vista para actualizar un producto existente.
    """
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        form = ProductoForm(instance=producto)
        return render(request, 'bike/actualizar_producto.html', {'form': form, 'producto': producto})

    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
        return render(request, 'bike/actualizar_producto.html', {'form': form, 'producto': producto})

class EliminarProductoView(View):
    """
    Vista para eliminar un producto.
    """
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        return render(request, 'bike/confirmar_eliminar_producto.html', {'producto': producto})

    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return redirect('lista_productos')

# Vista para ver detalles de una boleta de compra
class DetalleBoletaView(View):
    """
    Vista para ver detalles de una boleta de compra.
    """
    def get(self, request, pk):
        boleta = get_object_or_404(Boleta, pk=pk)
        total = sum(detalle.subtotal() for detalle in boleta.detalles_compra.all())
        return render(request, 'bike/detalle_boleta.html', {'boleta': boleta, 'total': total})

# Vista para listar y crear productos a través de una API RESTful
class ProductoListCreateAPIView(generics.ListCreateAPIView):
    """
    Vista para listar y crear productos a través de una API RESTful.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Vista para mostrar detalles de un producto a través de una API RESTful
class ProductoDetailAPIView(generics.RetrieveAPIView):
    """
    Vista para mostrar detalles de un producto a través de una API RESTful.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Vista para mostrar las compras realizadas por un cliente
@method_decorator(login_required, name='dispatch')
class ComprasClienteView(ListView):
    """
    Vista para mostrar las compras realizadas por un cliente.
    """
    model = Boleta
    template_name = 'bike/compras_cliente.html'
    context_object_name = 'boletas'

    def get_queryset(self):
        cliente = self.request.user.cliente
        return Boleta.objects.filter(cliente=cliente).order_by('-fecha_compra')

# Vista para mostrar el carrito de compras del cliente
@method_decorator(login_required, name='dispatch')
class CarritoCompraView(View):
    """
    Vista para mostrar el carrito de compras del cliente.
    """
    def get(self, request):
        try:
            cliente = request.user.cliente
            carrito = Carrito.objects.get(cliente=cliente)
            productos = carrito.carritoproducto_set.all()
            total = sum(item.producto.precio * item.cantidad for item in productos)
            return render(request, 'bike/carrito_compra.html', {'carrito': carrito, 'productos': productos, 'total': total})
        except Carrito.DoesNotExist:
            messages.error(request, 'El cliente no tiene un carrito asociado.')
            return redirect('crear_carrito')
        except Cliente.DoesNotExist:
            messages.error(request, 'El usuario no tiene un perfil de cliente asociado.')
            return redirect('index')

# Vista para agregar un producto al carrito de compras del cliente
@method_decorator(login_required, name='dispatch')
class AgregarAlCarritoView(View):
    """
    Vista para agregar un producto al carrito de compras del cliente.
    """
    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        cliente = request.user.cliente
        carrito, created = Carrito.objects.get_or_create(cliente=cliente)
        carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)

        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad <= producto.stock:
            carrito_producto.cantidad += cantidad
            carrito_producto.save()
            producto.stock -= cantidad
            producto.save()
            messages.success(request, f'Se agregaron {cantidad} {producto.nombre} al carrito.')
        else:
            messages.warning(request, f'No hay suficiente stock disponible para agregar {cantidad} {producto.nombre}.')

        return redirect('carrito_compra')

# Vista para eliminar un producto del carrito de compras del cliente
@method_decorator(login_required, name='dispatch')
class EliminarDelCarritoView(View):
    """
    Vista para eliminar un producto del carrito de compras del cliente.
    """
    def post(self, request, pk):
        carrito_producto = get_object_or_404(CarritoProducto, pk=pk)
        carrito_producto.producto.stock += carrito_producto.cantidad
        carrito_producto.producto.save()
        carrito_producto.delete()
        return redirect('carrito_compra')

# Vista para crear el carrito de compras del cliente
@method_decorator(login_required, name='dispatch')
class CrearCarritoView(View):
    """
    Vista para crear el carrito de compras del cliente.
    """
    def get(self, request):
        cliente = request.user.cliente
        carrito, created = Carrito.objects.get_or_create(cliente=cliente)
        if created:
            messages.success(request, 'Carrito creado con éxito.')
        else:
            messages.info(request, 'Ya tienes un carrito.')
        return redirect('carrito_compra')

# Vista para solicitar restablecer la contraseña del usuario
def password_reset_request(request):
    """
    Vista para solicitar restablecer la contraseña del usuario.
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email="noreply@example.com",
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt'
            )
            messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})
