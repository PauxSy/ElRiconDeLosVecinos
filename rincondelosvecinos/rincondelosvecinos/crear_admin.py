import os
import django
from django.contrib.auth.hashers import make_password

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rincondelosvecinos.settings')
django.setup()

from rincondelosvecinos.models import Administrador  # Importa tu modelo de administrador

# Crea un administrador
def crear_administrador(email, rut, contrasena):
    contrasena_encriptada = make_password(contrasena)  # Encripta la contraseña
    admin = Administrador(
        email=email,
        rut=rut,  # Usa los campos definidos en el modelo
        contrasena=contrasena_encriptada,
    )
    admin.save()
    print(f"Administrador con email {email} creado con éxito.")

# Llama a la función con los datos del administrador
crear_administrador(
    email="admin@ejemplo.com",
    rut="12345678-9",  # Proporciona un RUT válido
    contrasena="admin123"
)
