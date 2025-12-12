from django import forms
from .models import Comentario
from django_ckeditor_5.widgets import CKEditor5Widget


class ComentarioForm(forms.ModelForm):
    contenido = forms.CharField(widget=CKEditor5Widget(config_name='default') )

    class Meta:
        model = Comentario
        fields = ['contenido']