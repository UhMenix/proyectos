from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('bikes/', views.BikesView.as_view(), name='bikes'),
    path('api/', views.ApiView.as_view(), name='api'),
    path('login/', auth_views.LoginView.as_view(template_name='bike/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('productos/', views.ListaProductosView.as_view(), name='lista_productos'),
    path('productos/crear/', views.CrearProductoView.as_view(), name='crear_producto'),
    path('productos/<int:pk>/', views.VerProductoView.as_view(), name='ver_producto'),
    path('productos/<int:pk>/actualizar/', views.ActualizarProductoView.as_view(), name='actualizar_producto'),
    path('productos/<int:pk>/eliminar/', views.EliminarProductoView.as_view(), name='eliminar_producto'),
    path('carrito/', views.CarritoCompraView.as_view(), name='carrito_compra'),
    path('carrito/agregar/<int:pk>/', views.AgregarAlCarritoView.as_view(), name='agregar_al_carrito'),
    path('carrito/eliminar/<int:pk>/', views.EliminarDelCarritoView.as_view(), name='eliminar_del_carrito'),
    path('boleta/<int:pk>/', views.DetalleBoletaView.as_view(), name='detalle_boleta'),
    path('clientes/', views.ClientesView.as_view(), name='clientes'),
    path('api/productos/', views.ProductoListCreateAPIView.as_view(), name='producto-list-create'),
    
]
