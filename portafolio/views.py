from django.shortcuts import render , redirect
from .models import Proyecto
from blog.models import Post


from django.http import HttpResponse
from  .form   import ContactForm


from django.contrib import messages
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail , Email
from dotenv import load_dotenv

load_dotenv()
def enviar_correo(nombre, email, asunto, mensaje):
    api_key = os.environ.get("SENDGRID_API_KEY")
    sender_email = os.environ.get("EMAIL_SENDER")
    receiver_email = os.environ.get("EMAIL_RECEIVER")
    
    subject = f"Contacto web: {nombre} - {asunto}"
    body = f"{mensaje}\n\nDe: {nombre} <{email}>"

    message = Mail(
        from_email=sender_email,
        to_emails=receiver_email,
        subject= f"Correo de {nombre} - {subject} ",
        html_content=f"<strong>{asunto}</strong> correo :{email}"
    
    )
    
    message.reply_to = Email(email)

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        return response.status_code == 202   # True si fue aceptado
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False


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
            print("eviado")
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




