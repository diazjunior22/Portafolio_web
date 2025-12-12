from django.contrib import admin
from .models import Post, Categoria
from django.utils.html import format_html

# Register your models here.


class PostsAdmin(admin.ModelAdmin):
    fields = [
        "titulo",
        "slug",
        "imagen",      # 👈 lo movemos arriba
        "contenido",
        "categoria",
        "publicado",
        "creado",
    ]
    list_display = ('titulo', 'publicado', 'creado', 'actualizado', 'categoria', 'image_tag')
    list_filter = ('publicado', 'categoria')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}  #esto es para cuando escriba algo en titulo se escriba igual en el slug
    date_hierarchy = 'creado' #
    ordering = ('-creado',)
    readonly_fields = ('image_tag',) # Make sure image_tag is read-only

    def image_tag(self, obj):
        if obj.imagen and obj.imagen.url:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="100" height="100" />', obj.imagen.url)
        # </a><br/><a href="{0}" target="_blank">{0}</a>'
        return "No Image"
    image_tag.short_description = 'Image Preview'


admin.site.register(Post,PostsAdmin)
admin.site.register(Categoria)