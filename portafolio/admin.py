from django.contrib import admin
from .models import Proyecto , Mensaje , Cliente

from django.utils.html import format_html


    
class ProyectoAdmin(admin.ModelAdmin):
    # columnas que aparecen en la lista
    list_display = ("id", "titulo", "descripcion", "image_tag", "url" , "visitar")
    #readonly_fields = ("url",)

    # convierte en enlace clickeable
    list_display_links = ("titulo",)

    # permite editar directo desde la lista
    list_editable = ("descripcion",)

    # barra de búsqueda
    search_fields = ("titulo", "descripcion")

    # filtros laterales
    list_filter = ("id",)  
    readonly_fields = ('image_tag',)

    def visitar(self, obj):
        return format_html('<a href="{}" target="_blank">Visitar</a>', obj.url)

    visitar.short_description = "VISITAR"

    def image_tag(self, obj):
        if obj.image and obj.image.url:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150" height="auto" /></a><br/><a href="{0}" target="_blank">{0}</a>', obj.image.url)
        return "No Image"
    image_tag.short_description = 'Image Preview'
        

class  MensajeAdmin(admin.ModelAdmin):
    # columnas que aparecen en la lista
    list_display = ("id", "asunto", "mensaje" ,'cliente__email', 'cliente_nombre' )

    def cliente_email(self, obj):
        return obj.cliente.email
    cliente_email.short_description = 'Email'
    def cliente_nombre(self, obj):
        return obj.cliente.email
    cliente_nombre.short_description = 'Nombre'
    list_display_links = ("cliente__email",)
    
    list_filter = ()  

    
class  ClienteAdmin(admin.ModelAdmin):
    # columnas que aparecen en la lista
    list_display = ('nombre' , 'email')


admin.site.register(Mensaje,MensajeAdmin)
admin.site.register(Cliente,ClienteAdmin)

    
admin.site.register(Proyecto , ProyectoAdmin )
# Register your models here.
