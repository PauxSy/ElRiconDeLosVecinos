from django.contrib import admin
from rincondelosvecinos.models import Administrador
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

class AdministradorAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Encripta la contraseña antes de guardar
        if form.cleaned_data['contrasena']:
            obj.contrasena = make_password(form.cleaned_data['contrasena'])
        super().save_model(request, obj, form, change)

admin.site.register(Administrador, AdministradorAdmin)

def verificar_admin(email, contrasena):
    try:
        admin = Administrador.objects.get(email=email)
        if check_password(contrasena, admin.contrasena):
            return True  # Contraseña válida
        else:
            return False  # Contraseña incorrecta
    except Administrador.DoesNotExist:
        return False  # Administrador no encontrado