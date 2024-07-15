from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='bike/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='bike/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='bike/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='bike/password_reset_complete.html'), name='password_reset_complete'),
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
    path('carrito/crear/', views.CrearCarritoView.as_view(), name='crear_carrito'),
    path('boleta/<int:pk>/', views.DetalleBoletaView.as_view(), name='detalle_boleta'),
    path('clientes/', views.ClientesView.as_view(), name='clientes'),
    path('api/productos/', views.ProductoListCreateAPIView.as_view(), name='producto-list-create'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('cliente/compras/', views.ComprasClienteView.as_view(), name='compras_cliente'),  
    path('api/productos/create/', views.ProductoListCreateAPIView.as_view(), name='producto-create'),
    path('confirmar_compra/', views.confirmar_compra, name='confirmar_compra'),
    path('agregar-al-carrito/<int:pk>/', views.agregar_al_carrito, name='agregar_al_carrito'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
