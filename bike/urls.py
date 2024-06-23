from django.urls import path
from .views import  index, about, contact, bikes,api, clientes,listadoSQL, login, register, tienda, agregar_al_carrito


urlpatterns = [
    path('', index, name='index'),
    path('about', about, name='about'),
    path('contact',contact,name='contact'),
    path('bikes',bikes,name='bikes'),
    path('api',api, name='api'),
    path('clientes',clientes, name='clientes' ),
    path('listadoSQL',listadoSQL, name='listadoSQL'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('', tienda, name='tienda'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    
]

  
