from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente,Genero,Producto, Carrito, CarritoProducto
# Create your views here.



def index(request):
    return render(request, 'bike/index.html')

def about(request):
    return render(request, 'bike/about.html')

def contact(request):
    return render(request, 'bike/contact.html')    

def bikes(request):
    return render(request,'bike/bikes.html')

def api(request):
    return render(request, 'bike/api.html') 

def login(request):
    return render(request, 'bike/login.html') 

def register(request):
    return render(request, 'bike/register.html') 

def clientes(request):
    
    clientes = Cliente.objects.all()  
    context={"clientes":clientes}
    return render(request, 'bike/clientes.html', context)
def listadoSQL(request):

    clientes =Cliente.objects.raw('SELECT * FROM clientes_cliente')
    print(clientes)
    context={"clientes":clientes}
    return render(request, 'bike/listadoSQL.html', context)
def tienda(request):

    productos = Producto.objects.all()
    return render(request, 'tienda.html', {'productos': productos})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(id=request.session.get('carrito_id'))
    if created:
        request.session['carrito_id'] = carrito.id
    carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        carrito_producto.cantidad += 1
        carrito_producto.save()
    return redirect('tienda')

