from django.shortcuts import render , redirect

from .models import Proyecto
from django.http import HttpResponse

from  .form   import ContactForm


from django.core.mail import EmailMessage

from blog.models import Post




from django.contrib import messages


# Create your views here.


def enviar_correo(nombre, email, asunto, mensaje):
            EmailMessage(
                subject = f'CONTACTO EMAILL {nombre}' ,
                body = f'{mensaje} + {asunto}' ,
                from_email='juniordiazpalacio9@gmail.com',
                to = ['juniordiazpalacio9@gmail.com'],
                cc = [],
                reply_to=[email]
                
                
            ).send()



def home(request):
    post = Post.objects.filter(publicado=True).order_by('-creado')[:3]
    total_post =  Post.objects.filter(publicado=True).count()
    proyecto  = Proyecto.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            enviar_correo(nombre, email, asunto, mensaje)
            messages.success(request, "✅ Tu mensaje fue enviado con éxito. ¡Gracias por contactarme!")
            return redirect('home')
        else:
                        messages.error(request, "❌ Ocurrió un error. Revisa los datos e inténtalo nuevamente.")

    else:
        form = ContactForm()
    
    context = {
        'proyecto':proyecto ,
        'form' : form,
        'post_blog' : post,
        'total_posts' : total_post > 3
        
        }
    return render(request, 'portafolio/inicio.html' , context)




