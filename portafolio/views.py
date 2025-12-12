from django.shortcuts import render , redirect
from .models import Proyecto
from blog.models import Post


from  .form   import ContactForm


from django.contrib import messages



from .models import Cliente, Mensaje



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
            contenido = form.cleaned_data['mensaje']
            cliente, creado = Cliente.objects.get_or_create(email=email, defaults={'nombre': nombre})

            # Crear mensaje asociado al cliente
            Mensaje.objects.create(
                cliente=cliente,
                asunto=asunto,
                mensaje=contenido
            )
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




