from django.contrib import admin
from .models import Proyecto

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
        
    
    
admin.site.register(Proyecto , ProyectoAdmin )
# Register your models here.
