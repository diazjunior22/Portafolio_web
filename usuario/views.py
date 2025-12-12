from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .form import CustomUserCreationForm, LoginForm

from .models import CustomUser

#process of verificacion de cuenta

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string #para pasar un html a un string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

#correo
import os 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail , Email
from dotenv import load_dotenv
load_dotenv()

import resend


resend.api_key = os.getenv('resend')



def enviar_correo(email, asunto, mensaje):
    r = resend.Emails.send({
    "from": "no-reply@jxdev.xyz",
    "to": email ,
    "subject": asunto,
    "html": mensaje,
    })




def register(request):
    # Si el usuario ya está autenticado, lo redirigimos a la página principal.
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.user.is_authenticated:
        return redirect('listaPost')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            print(email)
            user = form.save()
            sitio_actual = get_current_site(request)
            asunto = 'Activa tu cuenta' 
            contenido = render_to_string('usuario/verificacion.html', {
                'user' : user,
                'domain' : sitio_actual,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email =  email
            enviar_correo(to_email,asunto, contenido)
            
            return redirect('/auth/login/?command=verification&email='+email)
            
            return redirect(next_url or 'listaPost') 
        else:
            # Los errores específicos del formulario se mostrarán en la plantilla.
            # Este es un mensaje de error general.
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'usuario/register.html', {'form': form})


def login_view(request):
    """
    Gestiona el inicio de sesión de los usuarios con una vista personalizada.
    """
    # Si el usuario ya está autenticado, no tiene sentido mostrarle la página de login.
    if request.user.is_authenticated:
        return redirect('listaPost')

    # Si la petición es POST, el usuario ha enviado el formulario.
    if request.method == 'POST':
        # Instanciamos nuestro LoginForm personalizado. AuthenticationForm requiere el objeto `request`.
        form = LoginForm(request, data=request.POST)
        
        # `is_valid()` en un AuthenticationForm comprueba que las credenciales son correctas.
        if form.is_valid():
            # Si las credenciales son válidas, `form.get_user()` nos devuelve el objeto de usuario.
            user = form.get_user()
            
            # `login()` crea la sesión para el usuario. Es una función de seguridad de Django.
            login(request, user)
                        
            # Si el usuario intentó acceder a una página protegida antes de hacer login,
            # Django guarda esa URL en `next`. Si existe, lo redirigimos allí.
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Si no, lo enviamos a la página principal.
            return redirect('listaPost')
            
    # Si la petición es GET, creamos un formulario vacío.
    else:
        form = LoginForm()
        
    # Renderizamos la plantilla, pasándole el formulario.
    return render(request, 'usuario/login.html', {'form': form})


def logout_view(request):
    """
    Cierra la sesión del usuario actual.
    """
    # `logout` es la función de Django que se encarga de limpiar la sesión del usuario.
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    # Redirigimos al usuario a la página principal.
    return redirect('listaPost')

def activate(request, uidb64, token):
    
    try :
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Tu Cuenta Ha Sido Activada')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
    