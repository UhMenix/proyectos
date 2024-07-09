from django.contrib import admin
from django.urls import path
from bike import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('bikes/', views.bikes, name='bikes'),
    path('api/', views.api, name='api'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('clientes/', views.clientes, name='clientes'),
    path('listadoSQL/', views.listadoSQL, name='listadoSQL'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('actualizar_producto/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('ver_producto/<int:pk>/', views.ver_producto, name='ver_producto'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito_compra/', views.carrito_compra, name='carrito_compra'),
    path('eliminar_del_carrito/<int:detalle_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('detalle_boleta/<int:boleta_id>/', views.detalle_boleta, name='detalle_boleta'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
]
