# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from rest_framework import generics
from .models import Producto, Boleta, DetalleCompra, Cliente
from .forms import ProductoForm
from .serializers import ProductoSerializer

class IndexView(View):
    def get(self, request):
        return render(request, 'bike/index.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'bike/about.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'bike/contact.html')

class BikesView(ListView):
    model = Producto
    template_name = 'bike/bikes.html'
    context_object_name = 'productos'
    paginate_by = 12  # 12 productos por página

class ApiView(View):
    def get(self, request):
        return render(request, 'bike/api.html')

class ClientesView(ListView):
    model = Cliente
    template_name = 'bike/clientes.html'
    context_object_name = 'clientes'

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'bike/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        return render(request, 'bike/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'bike/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        return render(request, 'bike/login.html', {'form': form})

class ListaProductosView(ListView):
    model = Producto
    template_name = 'bike/lista_productos.html'
    context_object_name = 'productos'

class CrearProductoView(View):
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
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        return render(request, 'bike/ver_producto.html', {'producto': producto})

class ActualizarProductoView(View):
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
    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        return render(request, 'bike/confirmar_eliminar_producto.html', {'producto': producto})

    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return redirect('lista_productos')

@method_decorator(login_required, name='dispatch')
class CarritoCompraView(View):
    def get(self, request):
        boleta = Boleta.objects.filter(cliente=request.user.cliente, estado_pedido='recibido').first()
        total = 0
        if boleta:
            total = sum(detalle.subtotal() for detalle in boleta.detalles_compra.all())
        return render(request, 'bike/carrito_compra.html', {'boleta_compra': boleta, 'total': total})

@method_decorator(login_required, name='dispatch')
class AgregarAlCarritoView(View):
    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        boleta, created = Boleta.objects.get_or_create(cliente=request.user.cliente, estado_pedido='recibido')
        detalle, detalle_created = DetalleCompra.objects.get_or_create(boleta=boleta, producto=producto)

        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad <= producto.stock:
            detalle.cantidad += cantidad
            detalle.precio_unitario = producto.precio
            detalle.save()
            producto.stock -= cantidad
            producto.save()
            messages.success(request, f'Se agregaron {cantidad} {producto.nombre} al carrito.')
        else:
            messages.warning(request, f'No hay suficiente stock disponible para agregar {cantidad} {producto.nombre}.')

        return redirect('carrito_compra')

@method_decorator(login_required, name='dispatch')
class EliminarDelCarritoView(View):
    def post(self, request, pk):
        detalle = get_object_or_404(DetalleCompra, pk=pk)
        detalle.producto.stock += detalle.cantidad
        detalle.producto.save()
        detalle.delete()
        return redirect('carrito_compra')

@method_decorator(login_required, name='dispatch')
class DetalleBoletaView(View):
    def get(self, request, pk):
        boleta = get_object_or_404(Boleta, pk=pk)
        total = sum(detalle.subtotal() for detalle in boleta.detalles_compra.all())
        return render(request, 'bike/detalle_boleta.html', {'boleta': boleta, 'total': total})


class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all() 
    serializer_class = ProductoSerializer
