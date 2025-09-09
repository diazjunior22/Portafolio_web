from django.shortcuts import render , redirect

from .models import Proyecto
from django.http import HttpResponse

from  .form   import ContactForm


from django.core.mail import EmailMessage

from blog.models import Post


#784303315bfb2d606d4296bc75dd96c1

from django.contrib import messages

import  requests

import os 
from dotenv import load_dotenv


load_dotenv()
# Create your views here.


# def enviar_correo(nombre, email, asunto, mensaje):
#             EmailMessage(
#                 subject = f'CONTACTO EMAILL {nombre}' ,
#                 body = f'{mensaje} + {asunto}' ,
#                 from_email='juniordiazpalacio9@gmail.com',
#                 to = ['juniordiazpalacio9@gmail.com'],
#                 cc = [],
#                 reply_to=[email]
                
                
#             ).send()


import mailtrap as mt

client = mt.MailtrapClient(token=os.getenv("MAILTRAP_API_KEY"))

def enviar_correo(nombre, email, asunto, mensaje):
    token = "d645d0fae3fca7ab6351e54d83591802"

    # payload = {
    #     "from": {"email": "hello@demomailtrap.com", "name": nombre},
    #     "to": [{"email": "juniordiazpalacio9@gmail.com"}],
    #     "reply_to": [{"email": email}],
    #     "subject": f"CONTACTO EMAIL {nombre} - {asunto}",
    #     "text": mensaje,
    #     "category": "Formulario Web"
    # }# Pon aquí tu API Token de Mailtrap (Email Sending > API Tokens)

    # headers = {
    #         "Authorization": f"Bearer {token}",
    #         "Content-Type": "application/json"
    # }
    # response = requests.post( url, headers=headers, json=payload)

    mail = mt.Mail(
        sender=mt.Address(email="juniordiazpalacio9@gmail.com", name=nombre),  
        to=[mt.Address(email="juniordiazpalacio9@gmail.com")],          
        subject=f"CONTACTO EMAIL {nombre} - {asunto} Responder a: {email}",
        text=f"De: {nombre} <{email}>\n\nMensaje:\n{mensaje}",
        category="Formulario Web",
    )
    response = client.send(mail)
    return response 


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




