from django.contrib import admin
from .models import Proyecto

from django.utils.html import format_html


    
class ProyectoAdmin(admin.ModelAdmin):
    # columnas que aparecen en la lista
    list_display = ("id", "titulo", "descripcion", "image", "url" , "visitar")
    #readonly_fields = ("url",)

    # convierte en enlace clickeable
    list_display_links = ("titulo",)

    # permite editar directo desde la lista
    list_editable = ("descripcion",)

    # barra de búsqueda
    search_fields = ("titulo", "descripcion")

    # filtros laterales
    list_filter = ("id",)  
    def visitar(self, obj):
        return format_html('<a href="{}" target="_blank">Visitar</a>', obj.url)

    visitar.short_description = "VISITAR"
        
    
    
admin.site.register(Proyecto , ProyectoAdmin )
# Register your models here.
