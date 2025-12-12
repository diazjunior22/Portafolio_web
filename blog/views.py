from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post , Comentario
from django.db.models import Q
from .form import ComentarioForm
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse

# Create your views here.
def listaPost(request):
    posts = Post.objects.all()
    return render(request, 'blog/lista.html', {'posts': posts})





@login_required(login_url='login')
def comentar(request,id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            comentario = form_comentario.save(commit=False)
            comentario.usuario = request.user
            comentario.post = post
            comentario.save()
            print('comentario guardado')
            return redirect('detallePost', id=id)
    



def detallePost(request, id):
    post = get_object_or_404(Post, id=id)
    comentario  = Comentario.objects.filter(post_id=id).order_by('-creado')
    form_comentario = ComentarioForm()
    return render(request, 'blog/detalle.html', {'post': post , 'comentario' : comentario , 'form' : form_comentario})
    #$return render(request
    # , 'blog/detalle.html', {'post': post})
    
    
def search(request):
    query = request.GET.get('q')
    posts = Post.objects.all()
    
    if query:
            posts = posts.filter(
            Q(titulo__icontains=query) | Q(contenido__icontains=query)
        )
            
    return render(request, "blog/lista.html", {
        "posts": posts,
        "query": query
    })