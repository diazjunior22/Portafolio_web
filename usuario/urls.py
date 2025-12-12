from django.urls import path
from . import views

# ==================================================================================
# BUENAS PRÁCTICAS PARA URLs DE AUTENTICACIÓN
# ----------------------------------------------------------------------------------
# Mantener las URLs de autenticación agrupadas y claras es una buena práctica.
# Estamos usando vistas personalizadas para tener control total sobre la lógica
# y la experiencia de usuario, en lugar de las vistas genéricas de Django.
# ==================================================================================

urlpatterns = [
    # Ruta para el registro de nuevos usuarios.
    path('register/', views.register, name='register'),
    
    # Ruta para el inicio de sesión, que ahora apunta a nuestra vista `login_view`.
    path('login/', views.login_view, name='login'),
    
    # Ruta para cerrar la sesión, apuntando a nuestra vista `logout_view`.
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]



