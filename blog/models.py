from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django_ckeditor_5.fields import CKEditor5Field
from usuario.models import  CustomUser



# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    stug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.nombre



class Post(models.Model):    
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField(default='sin descripcion' ,null=True, blank=True)
    contenido  = CKEditor5Field("Content" , config_name='default', blank=True , null=True)
    imagen = CloudinaryField('image', folder='blog', blank=True, null=True , default='https://res.cloudinary.com/dmtqsct7k/image/upload/v1763242716/no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-coming-soon-sign-simple-nature-silhouette-in-frame-isolated-illustration-vector_awbgaz.jpg')
    creado = models.DateTimeField(default=timezone.now)
    actualizado = models.DateTimeField(auto_now=True)
    publicado =  models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE , verbose_name='Categoria')

    def __str__(self):
        return self.titulo





class Comentario(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True
                                )
    contenido = CKEditor5Field('contenido' , config_name='default')
    creado = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post-coments' )
    
    def __str__(self):
        return f'Comentario de {self.usuario.username}'



