from django.db import models

from django.utils import timezone



# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    stug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.nombre



class Post(models.Model):    
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    contenido  = models.TextField()
    imagen = models.ImageField(upload_to='blog/', blank=True, null=True , default="posts/default.jpg")
    creado = models.DateTimeField(default=timezone.now)
    actualizado = models.DateTimeField(auto_now=True)
    publicado =  models.BooleanField(default=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo



