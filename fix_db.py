import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portafolio_app.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Drop existing out-of-sync tables
    cursor.execute("DROP TABLE IF EXISTS blog_comentario CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS blog_post CASCADE;")
    cursor.execute("DROP TABLE IF EXISTS blog_categoria CASCADE;")
    
    # Remove migration history so Django thinks it needs to recreate them
    cursor.execute("DELETE FROM django_migrations WHERE app='blog';")

print("Se eliminaron las tablas antiguas de Railway. Todo listo para migrar de nuevo.")
