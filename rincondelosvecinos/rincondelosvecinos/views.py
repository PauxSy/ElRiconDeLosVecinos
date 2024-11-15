from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render #PRUEBA PARA VER SI CONECTA CON LA BD
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate 
from .models import Producto , Usuario
# ----------------
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

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

def vista_recuperarcontraseña(request):
    return render(request,'recuperarcontraseña.html')

# -----------kkk------------------

def enviar_correo(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            usuario = Usuario.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Recupera tu contraseña'
            token = default_token_generator.make_token(usuario)
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            link = f"http://{current_site.domain}/reset/{uid}/{token}/"
            message = render_to_string('email_recuperacion.html', {
                'user': usuario,
                'link': link,
            })
            send_mail(mail_subject, message, 'tucorreo@gmail.com', [email])
            messages.success(request, "Se ha enviado un enlace de recuperación a tu correo")
        except Usuario.DoesNotExist:
            messages.error(request, "No existe una cuenta con este correo")
    
    return render(request, 'cambiarcontraseña.html')



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
        return render(request, 'form_reset_password.html', {'usuario': usuario})
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



