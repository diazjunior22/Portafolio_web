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