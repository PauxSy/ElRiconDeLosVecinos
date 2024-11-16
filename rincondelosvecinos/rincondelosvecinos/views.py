from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render #PRUEBA PARA VER SI CONECTA CON LA BD
from django.shortcuts import render, redirect
from .models import Producto , Usuario
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse





def vista_recuperarcontraseña(request):
    if request.method == "POST":
        email = request.POST.get('email')

        # Validar si el correo existe en la base de datos
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(request, "No existe un usuario registrado con ese correo.")
            return render(request, 'recuperarcontraseña.html')

        # Construir el enlace para restablecer contraseña
        reset_link = request.build_absolute_uri(
            reverse('reset_password', args=[usuario.id])
        )

        # Enviar el correo con el enlace
        try:
            send_mail(
                subject="Recuperación de contraseña",
                message=f"Hola, para restablecer tu contraseña haz clic en el siguiente enlace: {reset_link}",
                from_email="tuemail@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "El correo se envió correctamente. Revisa tu bandeja de entrada.")
        except Exception as e:
            messages.error(request, f"Error al enviar el correo: {str(e)}")
    
    return render(request, 'recuperarcontraseña.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Usuario


def reset_password(request, user_id):
    if request.method == "POST":
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
            return render(request, 'reset_password.html', {'user_id': user_id})

        try:
            usuario = Usuario.objects.get(id=user_id)
            usuario.contrasena = nueva_contrasena  # Guardar la contraseña sin encriptar
            usuario.save()
            messages.success(request, "Tu contraseña ha sido actualizada con éxito.")
            return redirect('catalogo')
        except Usuario.DoesNotExist:
            messages.error(request, "El usuario no existe. Por favor, verifica tu información.")
            return render(request, 'reset_password.html', {'user_id': user_id})

    # Aquí asegúrate de pasar el user_id al contexto
    return render(request, 'reset_password.html', {'user_id': user_id})






# -----------kkk------------------

def vista_iniciouser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Busca el usuario en la base de datos
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.contrasena == password:
                # Inicio de sesión exitoso
                messages.success(request, "Inicio de sesión exitoso")
                return redirect('catalogo')  # Redirigir a la página de inicio
            else:
                messages.error(request, "Contraseña incorrecta")
        except Usuario.DoesNotExist:
            messages.error(request, "El email no está registrado")

    return render(request, 'inicioSesioónUser.html')    

# -----------kkk------------------

def vista_detalleproducto(request, id):
    # Obtén el producto con el id proporcionado en la URL
    producto = get_object_or_404(Producto, id=id)
    
    # Pasa el producto a la plantilla
    return render(request, 'detalleProducto.html', {'producto': producto})


def vista_catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})


def vista_registrouser(request):
    return render(request,'registroUser.html')

def vista_perfiluser(request):
    return render(request,'perfilUser.html')

def vista_historialuser(request):
    return render(request,'historialCompraUser.html')

# ---------------Admin---------------- 
def vista_inicioadmin(request):
    return render(request,'inicioAdmin.html')

def vista_reporteadmin(request):
    return render(request,'generarReportesAdmin.html')

def vista_agregarproductoadmin(request):
    return render(request,'agregarProductoAdmin.html')

def vista_inventario(request):
    return render(request,'verinventario.html')

def vista_actualizarproducto(request):
    return render(request,'actualizarProductoAdmin.html')


def vista_deshabilitarproducto(request):
    return render(request,'deshabilitarProductoAdmin.html')

def vista_actualizarstock(request):
    return render(request,'actualizarStock.html')


def vista_panelpromociones(request):
    return render(request,'crearPromocionAdmin.html')


def vista_registrovendedor(request):
    return render(request,'RegistroVendedor.html')


def vista_registrobodeguero(request):
    return render(request,'Registrobodeguero.html')

def vista_dashboard(request):
    return render(request,'dashboard.html')


# ---------------vendedor---------------- 
def vista_iniciovendedor(request):
    return render(request,'inicioVendedor.html')

def vista_panelvendedor(request):
    return render(request,'panelvendedor.html')


# ---------------bodeguero---------------- 
def vista_iniciobodeguero(request):
    return render(request,'inicioBodeguero.html')

def vista_panelbodeguero(request):
    return render(request,'panelBodeguero.html')


#--------------vistas_añadidas_extras_---------------

#para que puedan seleccionar su tipo de cuenta antes de iniciar sesión en catalogo
# (aun no añadida a catalogo 
# porque pau esta trabajando en ella)

def vista_seleccionarcuentainicio(request):
    return render(request,'seleccionarcuentainicio.html')

#para que puedan seleccionar su tipo de cuenta al pinchar en crear cuenta como admin
def vista_elegircuentaacrear(request):
    return render(request,'elegircuentaacrear.html')



