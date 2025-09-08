from django.contrib import admin
from .models import Post, Categoria
# Register your models here.


class PostsAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicado', 'creado', 'actualizado', 'id_categoria')
    list_filter = ('publicado', 'id_categoria')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}  #esto es para cuando escriba algo en titulo se escriba igual en el slug
    date_hierarchy = 'creado' #
    ordering = ('-creado',)


admin.site.register(Post,PostsAdmin)
admin.site.register(Categoria)