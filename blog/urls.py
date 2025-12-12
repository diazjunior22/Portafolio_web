from django.urls import path
from . import views
urlpatterns = [
    path('' , views.listaPost , name='listaPost'),
    path('Post/<int:id>' , views.detallePost , name='detallePost'),
    path('search/', views.search , name='search'),
    path('comentar/<int:id>' , views.comentar , name='comentar')

]
