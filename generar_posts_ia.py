import os
import django
import sys
import random
from django.utils import timezone
from django.utils.text import slugify

# =========== CONFIGURACIÓN ===========
# Configurar el script para usar el entorno de nuestro proyecto Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portafolio_app.settings")
django.setup()

# Importar los modelos después de la configuración de Django
from blog.models import Post, Categoria

# Intentamos importar cloudinary para subir la imagen 
# exactamente como el modelo lo requiere (en la carpeta 'blog')
try:
    import cloudinary
    import cloudinary.uploader
    has_cloudinary = True
except ImportError:
    has_cloudinary = False
    print("⚠️ Módulo de Cloudinary no encontrado.")

# =========== DATOS GENERADOS CON IA ===========
# Categorías de prueba
categorias_nombres = ["Inteligencia Artificial", "Desarrollo Web", "Tecnología", "Tutoriales"]

# Datos de los posts generados con un estilo profesional / IA.
posts_data = [
    {
        "titulo": "El Futuro del Desarrollo Web Impulsado por IA",
        "descripcion": "Descubre cómo la Inteligencia Artificial está cambiando drásticamente la forma en la que diseñamos, escribimos y mantenemos el código moderno en 2024.",
        "contenido": "<h2>La evolución de la IA en la programación</h2><p>La IA ya no es solo una moda; es una herramienta fundamental en el día a día. Herramientas como GitHub Copilot o ChatGPT han demostrado que pueden acelerar nuestro trabajo y evitar que hagamos tareas repetitivas.</p><p>Como desarrolladores, nuestro deber no es preocuparnos, sino adaptarnos y aprovechar estas tecnologías para crear software más robusto, accesible y escalable.</p>",
        "imagen_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Dominando Animaciones Web con GSAP y ScrollTrigger",
        "descripcion": "Guía paso a paso para transformar sitios web estáticos en experiencias altamente dinámicas y visuales utilizando GSAP.",
        "contenido": "<h2>¿Qué es GSAP?</h2><p>GreenSock Animation Platform (GSAP) es el estándar definitivo en la industria para realizar animaciones web complejas con alto rendimiento.</p><p>Gracias a su plugin <strong>ScrollTrigger</strong>, realizar efectos al hacer scroll, como los vistos en la web de Apple o sitios premiados en Awwwards, ahora es rápido y sorprendentemente fácil de implementar.</p>",
        "imagen_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Optimización Avanzada con PostgreSQL en Django",
        "descripcion": "Las mejores estrategias, prácticas y consultas optimizadas usando PostgreSQL, y por qué es la piedra angular del backend moderno.",
        "contenido": "<h2>Por qué elegimos PostgreSQL</h2><p>PostgreSQL ofrece una estabilidad y un potencial inmenso a nivel de base de datos relacionales, sobre todo en aplicaciones complejas.</p><p>En Django, aprovechar al máximo PostgreSQL usando uniones <code>select_related</code> y el soporte nativo para campos avanzados como JSON o de texto completo te permite llevar cualquier aplicación al siguiente nivel sin tener que migrar a bases de datos en memoria inmediatamente.</p>",
        "imagen_url": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?q=80&w=800&auto=format&fit=crop"
    },
    {
        "titulo": "Microservicios vs Monolitos: La Decisión Crucial",
        "descripcion": "Un análisis profundo y transparente de las arquitecturas de software más utilizadas. Cuándo usar cuál para no ahogarte en complejidad.",
        "contenido": "<h2>Desmitificando las arquitecturas</h2><p>El hype suele decir que debemos realizar todo en Microservicios o Arquitecturas Serverless. Sin embargo, para más del 80% de startups nuevas, lanzar un Monolito bien acoplado en un framework como Django es infinitamente superior y rápido.</p><p>Aprender cuándo dividir tus aplicaciones en microservicios, generalmente cuando el equipo es demasiado grande y la escalabilidad necesita fragmentación vertical, es el diferenciador de un arquitecto nivel Senior.</p>",
        "imagen_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=800&auto=format&fit=crop"
    }
]

def poblar_base_de_datos():
    print("--------------------------------------------------")
    print("🤖 Iniciando la generación e inserción de Posts...")
    print("--------------------------------------------------\n")

    # 1. Crear las categorías iterando sobre nuestra lista
    categorias_obj = []
    for nombre in categorias_nombres:
        slug = slugify(nombre)
        # Nota: en tu modelo Categoria, el slug se llama 'stug'
        cat, created = Categoria.objects.get_or_create(
            nombre=nombre, 
            defaults={'stug': slug}
        )
        categorias_obj.append(cat)
        if created:
            print(f"✅ Categoría creada: {nombre}")

    print("\n--------------------------------------------------")
    print(f"📦 Se insertarán {len(posts_data)} posts en la base de datos...")
    
    # 2. Iterar sobre todos los datos y crear los Posts
    for data in posts_data:
        # Generar un slug único basado en el título
        slug_base = slugify(data["titulo"])
        slug = slug_base
        contador = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{slug_base}-{contador}"
            contador += 1

        cat = random.choice(categorias_obj)

        # Inicializar el Post
        post = Post(
            titulo=data["titulo"],
            slug=slug,
            descripcion=data["descripcion"],
            contenido=data["contenido"],
            categoria=cat,
            publicado=True,
            creado=timezone.now()
        )

        try:
            # Subir la imagen a Cloudinary desde la URL para que se guarde 
            # de acuerdo a como lo indica el modelo ('folder=blog')
            if has_cloudinary:
                print(f"🚀 Subiendo imagen a Cloudinary para: '{data['titulo']}'...")
                # Esto automáticamente descarga la imagen de splash y la envía a la carpeta "blog"
                respuesta_cloudinary = cloudinary.uploader.upload(data['imagen_url'], folder='blog')
                
                # Guardamos el identificador público generado
                post.imagen = respuesta_cloudinary['public_id'] 
            else:
                print(f"⚠️ Usando URL directa para '{data['titulo']}' debido a la falta de cloudinary...")
                post.imagen = data['imagen_url']
        except Exception as e:
            print(f"❌ Error al intentar subir la imagen para '{data['titulo']}': {e}")
            print("Guardando post sin la imagen personalizada (asume la de por defecto)...")

        post.save()
        print(f"✔️  Post guardado en DB: {post.titulo} (Cat: {cat.nombre})\n")

    print("\n🎉 ¡Proceso terminado! Todos los posts e imágenes se cargaron exitosamente.")


if __name__ == "__main__":
    poblar_base_de_datos()
