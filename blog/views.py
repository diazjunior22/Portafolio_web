from django.shortcuts import render , get_object_or_404
from .models import Post
from django.db.models import Q

from django.http import HttpResponse

# Create your views here.
def listaPost(request):
    posts = Post.objects.all()
    return render(request, 'blog/lista.html', {'posts': posts})




def detallePost(request, id):
    post = get_object_or_404(Post, id=id)
    
    return render(request, 'blog/detalle.html', {'post': post})
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