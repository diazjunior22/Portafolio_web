
# Register your models here.
from django.contrib import admin
from .models import CustomUser

from django.contrib.auth.admin import UserAdmin 
# Register your models here.

#this class is used to customize the admin interface for the Account model
#it inherits from UserAdmin to use the built-in user admin features
class AccountAdmin(UserAdmin):
    #para mostrar el modelo en el panel de administración
    list_display = ('username', 'email',   'last_login', 'is_admin', 'is_active', 'is_staff', 'is_superadmin' ,'password')
    list_display_links = ('username', 'email',)
    #search_fields = ('username', 'email', 'first_name', 'last_name')
   
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, AccountAdmin)
