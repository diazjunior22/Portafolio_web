from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.



class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    image = CloudinaryField('image', folder='portafolio/images')
    url = models.URLField(blank=True)

    def __str__(self):
        return self.titulo
    
    
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} {self.email}'

class Mensaje(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mensajes')
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asunto} - {self.cliente.nombre}"