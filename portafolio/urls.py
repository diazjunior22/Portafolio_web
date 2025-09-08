from django.urls import path
from portafolio import views




urlpatterns = [
    path("" , views.home , name="home")
]
