import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portafolio_app.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DROP SCHEMA public CASCADE;")
    cursor.execute("CREATE SCHEMA public;")
    cursor.execute("GRANT ALL ON SCHEMA public TO public;")

print("¡La base de datos de Railway ha sido limpiada por completo con éxito!")
