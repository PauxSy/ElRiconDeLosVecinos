from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render #PRUEBA PARA VER SI CONECTA CON LA BD
from django.shortcuts import render, redirect
from .models import Producto , Usuario
# ----------------
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages

# -----------kkk------------------



from django.core.mail import send_mail  # Importa la función para enviar correos
from django.contrib import messages
from django.shortcuts import render


def vista_recuperarcontraseña(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Obtén el correo electrónico del formulario
        if email:
            try:
                # Enviar un correo simple
                send_mail(
                    'Recuperación de contraseña',
                    'Hola, este es un mensaje de prueba para recuperar tu contraseña.',
                    'tu_correo@gmail.com',  # Reemplaza con tu correo configurado en settings.py
                    [email],
                    fail_silently=False,  # Cambia a True si no quieres mostrar errores
                )
                messages.success(request, 'El correo se envió correctamente. Revisa tu bandeja de entrada.')
            except Exception as e:
                messages.error(request, f'Error al enviar el correo: {str(e)}')
        else:
            messages.error(request, 'Por favor, ingresa un correo válido.')
    
    return render(request,'recuperarcontraseña.html')







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
            else:
                messages.error(request, "Contraseña incorrecta")
        except Usuario.DoesNotExist:
            messages.error(request, "El email no está registrado")

    return render(request, 'inicioSesioónUser.html')




from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None

    if usuario is not None and default_token_generator.check_token(usuario, token):
        if request.method == 'POST':
            nueva_contrasena = request.POST['nueva_contrasena']
            usuario.contrasena = nueva_contrasena
            usuario.save()
            messages.success(request, "Contraseña actualizada con éxito")
            return redirect('iniciouser')
        return render(request, 'reset_password.html', {'usuario': usuario})
    else:
        return HttpResponse('El enlace es inválido o ha expirado.')

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



