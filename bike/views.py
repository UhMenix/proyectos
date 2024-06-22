from django.shortcuts import render
from .models import Cliente,Genero
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

