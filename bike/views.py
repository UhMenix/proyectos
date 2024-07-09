from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Producto, BoletaCompra, DetalleCompra, Cliente
from .forms import ProductoForm, RegistroClienteForm

# Vistas principales
def index(request):
    return render(request, 'bike/index.html')

def about(request):
    return render(request, 'bike/about.html')

def contact(request):
    return render(request, 'bike/contact.html')

def bikes(request):
    return render(request, 'bike/bikes.html')

def api(request):
    return render(request, 'bike/api.html')

def login_view(request):
    return render(request, 'bike/login.html')

def register(request):
    form = RegistroClienteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirigir al inicio de sesión después del registro exitoso

    return render(request, 'bike/register.html', {'form': form})

# Funciones de clientes y listados
def clientes(request):
    clientes = Cliente.objects.all()
    context = {"clientes": clientes}
    return render(request, 'bike/clientes.html', context)

def listadoSQL(request):
    clientes = Cliente.objects.raw('SELECT * FROM clientes_cliente')
    context = {"clientes": clientes}
    return render(request, 'bike/listadoSQL.html', context)

# Funciones de autenticación
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('dashboard_admin')
                else:
                    return redirect('dashboard_cliente')
    else:
        form = AuthenticationForm()
    return render(request, 'bike/index.html', {'form': form})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')

# Funciones para el modelo Producto
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'bike/lista_productos.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'bike/crear_producto.html', {'form': form})

def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'bike/actualizar_producto.html', {'form': form})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'bike/confirmar_eliminar_producto.html', {'producto': producto})

def ver_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'bike/ver_producto.html', {'producto': producto})

# Funciones para el carrito de compras
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        if cantidad <= 0:
            # Manejar caso donde la cantidad no es válida
            return redirect('ver_producto', pk=producto.id)
        if cantidad > producto.stock:
            # Manejar caso donde la cantidad supera el stock disponible
            return redirect('ver_producto', pk=producto.id)

        # Verificar si el producto ya está en el carrito
        boleta_compra, created = BoletaCompra.objects.get_or_create(usuario=request.user, estado_pedido='Pendiente')
        detalle_compra, created = DetalleCompra.objects.get_or_create(boleta=boleta_compra, producto=producto)
        detalle_compra.cantidad += cantidad
        detalle_compra.precio_unitario = producto.precio
        detalle_compra.save()

        # Actualizar el stock del producto
        producto.stock -= cantidad
        producto.save()

        return redirect('detalle_boleta', boleta_id=boleta_compra.id)

    return render(request, 'bike/agregar_al_carrito.html', {'producto': producto})

@login_required
def carrito_compra(request):
    boleta_compra = BoletaCompra.objects.filter(usuario=request.user, estado_pedido='Pendiente').last()
    total = sum(detalle.cantidad * detalle.precio_unitario for detalle in boleta_compra.detalles_compra.all()) if boleta_compra else 0
    return render(request, 'bike/carrito_compra.html', {'boleta_compra': boleta_compra, 'total': total})

@login_required
def eliminar_del_carrito(request, detalle_id):
    detalle_compra = get_object_or_404(DetalleCompra, pk=detalle_id)
    if request.method == 'POST':
        # Actualizar el stock del producto al eliminarlo del carrito
        detalle_compra.producto.stock += detalle_compra.cantidad
        detalle_compra.producto.save()
        detalle_compra.delete()
        return redirect('carrito_compra')

    return render(request, 'bike/eliminar_del_carrito.html', {'detalle_compra': detalle_compra})

@login_required
def detalle_boleta(request, boleta_id):
    boleta = get_object_or_404(BoletaCompra, id=boleta_id)
    return render(request, 'bike/detalle_boleta.html', {'boleta': boleta})

# Nueva función para el registro de usuarios
def registrar_usuario(request):
    form = RegistroClienteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login') 

    return render(request, 'bike/registrar_usuario.html', {'form': form})
