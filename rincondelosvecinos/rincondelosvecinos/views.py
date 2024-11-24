from django.shortcuts import get_object_or_404, render #PRUEBA PARA VER SI CONECTA CON LA BD
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from rincondelosvecinos.forms import UsuarioForm
from .models import Producto , Usuario,Administrador
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from datetime import datetime, timedelta
import os
import hashlib
from django.utils.timezone import now, timedelta
from django.core.mail import EmailMultiAlternatives


def vista_iniciouser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            usuario = Usuario.objects.get(email=email)

            # Verificar si la cuenta está bloqueada
            if usuario.bloqueado:
                messages.error(request, "Tu cuenta está bloqueada. Por favor, restablece tu contraseña para desbloquearla.")
                return redirect('recuperarcontrasena')

            # Verificar si la cuenta no está activa (no confirmada)
            if not usuario.is_active:
                if usuario.fecha_token and now() - usuario.fecha_token > timedelta(hours=23):
                    # Reenviar correo de confirmación si han pasado más de 23 horas
                    uid = urlsafe_base64_encode(force_bytes(usuario.id))
                    token = default_token_generator.make_token(usuario)
                    activation_link = request.build_absolute_uri(
                        reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
                    )

                    # Enviar correo de confirmación
                    email_subject = "Confirma tu cuenta en El Rincón de los Vecinos"
                    email_body = render_to_string('email_confirmacion.html', {
                        'nombre_usuario': usuario.nombre,
                        'activation_link': activation_link,
                    })
                    email = EmailMultiAlternatives(
                        subject=email_subject,
                        body=email_body,
                        from_email="tuemail@gmail.com",
                        to=[usuario.email],
                    )
                    email.attach_alternative(email_body, "text/html")
                    email.send()

                    # Actualizar la fecha del token en la base de datos
                    usuario.fecha_token = now()
                    usuario.save()

                    messages.info(request, "Te hemos enviado un nuevo correo de confirmación. Revisa tu bandeja de entrada.")
                else:
                    # Recordar que debe confirmar su cuenta si han pasado menos de 23 horas
                    messages.warning(request, "Debes confirmar tu cuenta. Revisa el correo que te enviamos para activarla.")
                return redirect('iniciouser')

            # Verificar la contraseña
            if usuario.contrasena == encriptar_con_salt(password, usuario.salt):
                # Reiniciar intentos fallidos
                usuario.intentos_fallidos = 0
                usuario.bloqueado = False
                usuario.last_login = now()  # Actualizar el último inicio de sesión
                usuario.save()

                request.session['usuario_autenticado'] = True
                request.session['nombre_usuario'] = usuario.nombre
                request.session['primer_apellido'] = usuario.primer_apellido
                request.session['email'] = usuario.email                
                messages.success(request, "Inicio de sesión exitoso")
                return redirect('catalogo')

            else:
                # Incrementar intentos fallidos y bloquear si es necesario
                usuario.intentos_fallidos += 1
                if usuario.intentos_fallidos >= 3:
                    usuario.bloqueado = True
                usuario.save()
                messages.error(request, "Contraseña incorrecta")
        except Usuario.DoesNotExist:
            messages.error(request, "El email no está registrado")

    return render(request, 'inicioSesionUser.html')

def has_perm(self, perm, obj=None):
        """Permitir permisos básicos."""
        return True

def has_module_perms(self, app_label):
        """Permitir acceso a los módulos de la app."""
        return True

@property
def is_staff(self):
        """Definir si el usuario es parte del staff."""
        return False


#------version original 
# def vista_iniciouser(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         # Busca el usuario en la base de datos
#         try:
#             usuario = Usuario.objects.get(email=email)
#             if usuario.contrasena == password:
#                 # Inicio de sesión exitoso
#                 # Guarda el nombre y apellidos en la sesión
#                 request.session['nombre_usuario'] = usuario.nombre
#                 request.session['primer_apellido'] = usuario.primer_apellido

#                 messages.success(request, "Inicio de sesión exitoso")
#                 return redirect('catalogo')  # Redirigir a la página de inicio
#             else:
#                 messages.error(request, "Contraseña incorrecta")
#         except Usuario.DoesNotExist:
#             messages.error(request, "El email no está registrado")

#     return render(request, 'inicioSesionUser.html')



def vista_recuperarcontrasena(request):
    # Verificar si el usuario ya está autenticado
    if request.session.get("nombre_usuario") and request.session.get("primer_apellido"):
        messages.error(request, "Ya tienes una sesión iniciada. Por favor, cierra sesión antes de recuperar la contraseña.")
        return redirect("catalogo")

    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            messages.error(request, "Por favor, ingresa un correo electrónico.")
            return render(request, "recuperarcontrasena.html")

        # Buscar el usuario o administrador con el correo proporcionado
        usuario = Usuario.objects.filter(email=email).first()
        administrador = Administrador.objects.filter(email=email).first()

        if not usuario and not administrador:
            messages.error(request, "No existe una cuenta asociada a este correo.")
            return render(request, "recuperarcontrasena.html")

        # Generar un enlace de restablecimiento para usuario o administrador
        if usuario:
            user_type = "usuario"
            user_id = usuario.id
        else:
            user_type = "admin"
            user_id = administrador.id

        reset_link = request.build_absolute_uri(
            reverse("reset_password", args=[f"{user_type}_{user_id}"])
        )

        # Enviar el correo de recuperación
        try:
            send_mail(
                subject="Recuperación de contraseña",
                message=f"Hola, para restablecer tu contraseña haz clic en el siguiente enlace: {reset_link}",
                from_email="elrincondelosvecinoschile@gmail.com",  # Cambia por tu correo
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "El correo de recuperación fue enviado exitosamente. Revisa tu bandeja de entrada.")
        except Exception as e:
            messages.error(request, f"Hubo un error al enviar el correo: {str(e)}")

    return render(request, "recuperarcontrasena.html")


def reset_password(request, user_id):
    if request.method == "POST":
        nueva_contrasena = request.POST.get("nueva_contrasena")
        confirmar_contrasena = request.POST.get("confirmar_contrasena")

        # Validar si las contraseñas coinciden
        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
            return render(request, "reset_password.html", {"user_id": user_id})

        # Diferenciar entre usuario y administrador según el prefijo del ID
        if user_id.startswith("usuario_"):
            user_id = user_id.replace("usuario_", "")
            usuario_obj = Usuario.objects.filter(id=user_id).first()
        elif user_id.startswith("admin_"):
            user_id = user_id.replace("admin_", "")
            usuario_obj = Administrador.objects.filter(id=user_id).first()
        else:
            usuario_obj = None

        # Validar si existe el usuario o administrador correspondiente
        if not usuario_obj:
            messages.error(request, "El usuario o administrador no existe. Por favor, verifica tu información.")
            return render(request, "reset_password.html", {"user_id": user_id})

        # Generar un nuevo salt y encriptar la nueva contraseña
        salt = os.urandom(8).hex()
        nueva_contrasena_encriptada = hashlib.sha256((nueva_contrasena + salt).encode("utf-8")).hexdigest()

        # Actualizar la contraseña y desbloquear la cuenta si estaba bloqueada
        usuario_obj.contrasena = nueva_contrasena_encriptada
        usuario_obj.salt = salt
        if hasattr(usuario_obj, "intentos_fallidos"):
            usuario_obj.intentos_fallidos = 0  # Reiniciar intentos fallidos
            usuario_obj.bloqueado = False  # Desbloquear la cuenta

        usuario_obj.save()

        messages.success(request, "Tu contraseña ha sido actualizada con éxito y tu cuenta ha sido desbloqueada.")
        return redirect("catalogo")

    # Renderizar la plantilla con el ID en el contexto
    return render(request, "reset_password.html", {"user_id": user_id})






#--------FUNCIONALIDADES CARRITO----------------
def carrito(request):
    try:
        cart = request.session.get('cart', [])
        cart_items = []
        total = 0

        for item in cart:
            producto = Producto.objects.get(id=item['id'])
            subtotal = producto.precio * item['quantity']
            total += subtotal

            cart_items.append({
                'id': producto.id,
                'name': producto.nombre,
                'price': producto.precio,
                'quantity': item['quantity'],
                'subtotal': subtotal,
                'image': producto.img_url
            })

        return JsonResponse({
            'cart_items': cart_items,
            'total': total
        })
    except Exception as e:
        print(f"Error al cargar el carrito: {e}")
        return JsonResponse({'cart_items': [], 'total': 0})
    
def agregar_producto_carrito(request, producto_id):
    cantidad = request.POST.get('cantidad', 1)  # Por defecto 1 unidad
    producto = Producto.objects.get(id=producto_id)

    # Obtener el carrito de la sesión (o crear uno vacío si no existe)
    carrito = request.session.get('cart', [])

    # Verificar si el producto ya está en el carrito
    producto_en_carrito = next((item for item in carrito if item['id'] == producto.id), None)

    if producto_en_carrito:
        # Si el producto ya está, solo actualizamos la cantidad
        producto_en_carrito['quantity'] += int(cantidad)
    else:
        # Si el producto no está, lo agregamos al carrito
        carrito.append({
            'id': producto.id,
            'quantity': int(cantidad)
        })

    # Guardar el carrito actualizado en la sesión
    request.session['cart'] = carrito
    return redirect('carrito')  # Redirigir al carrito para mostrar los productos


def obtener_carrito(request):
    carrito = request.session.get('carrito', [])
    return JsonResponse({'cart_items': carrito})
#--------FUNCIONALIDADES CARRITO----------------

def vista_catalogo(request):
    query = request.GET.get('search', '')  
    if query:
        productos = Producto.objects.filter(nombre__icontains=query) 
    else:
        productos = Producto.objects.all()
        
    usuario_autenticado = request.session.get('email') is not None

    return render(request, 'catalogo.html', {
        'productos': productos,
        'query': query,
        'usuario_autenticado': usuario_autenticado,  # Agregar al contexto
    })

def vista_detalleproducto(request, id):
    # Obtén el producto con el id proporcionado en la URL
    producto = get_object_or_404(Producto, id=id)
    
    # Pasa el producto a la plantilla
    return render(request, 'detalleProducto.html', {'producto': producto})

def cerrar_sesion(request):
    # Limpia la sesión
    request.session.flush()
    # Crea un mensaje de éxito
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('catalogo')  # Redirige al catálogo


def vista_registrouser(request):
    return render(request,'registroUser.html')

def vista_perfiluser(request):
    # Verificar si el usuario está autenticado
    if not request.session.get('email'):
        messages.error(request, "Debes iniciar sesión para acceder a tu perfil.")
        return redirect('iniciouser')

    # Obtener el usuario autenticado usando el email de la sesión
    email = request.session['email']
    usuario = Usuario.objects.get(email=email)

    if request.method == 'POST':
        # Actualizar los campos con los datos enviados desde el formulario
        usuario.nombre = request.POST.get('nombre', usuario.nombre)
        usuario.primer_apellido = request.POST.get('primer_apellido', usuario.primer_apellido)
        usuario.segundo_apellido = request.POST.get('segundo_apellido', usuario.segundo_apellido)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.telefono = request.POST.get('telefono', usuario.telefono)
        usuario.direccion_particular = request.POST.get('direccion_particular', usuario.direccion_particular)
        usuario.direccion_facturacion = request.POST.get('direccion_facturacion', usuario.direccion_facturacion)

        # Guardar los cambios en la base de datos
        usuario.save()
        messages.success(request, "Tus datos se han actualizado exitosamente.")
        print({usuario.nombre})
        print({usuario.primer_apellido})

        return redirect('perfiluser')

    # Renderizar el formulario con los datos actuales del usuario
    return render(request, 'perfilUser.html', {'usuario': usuario})
def vista_historialuser(request):
    return render(request,'historialCompraUser.html')

# ---------------Admin---------------- 

def vista_inicioadmin(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        contrasena = request.POST.get('password')

        # Validación del formato del RUT
        if not validar_rut(rut):
            messages.error(request, 'El RUT ingresado no es válido.')
        try:
            # Consulta para encontrar al administrador por RUT
            admin = Administrador.objects.get(rut=rut)

            # Comparación directa de la contraseña
            if contrasena == admin.contrasena:
                return redirect('dashboard')  # Redirige al dashboard si todo es correcto
            else:
                messages.error(request, 'La contraseña ingresada es incorrecta.')
        except Administrador.DoesNotExist:
            messages.error(request, 'No está registrado.')

    return render(request, 'inicioAdmin.html')

def validar_rut(rut):
    """
    Valida el formato del RUT chileno. Ejemplo válido: 21270263-3
    """
    import re
    pattern = r'^\d{1,8}-[0-9kK]$'
    return re.match(pattern, rut) is not None

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

def vista_elegircuentaacrear(request):
    return render(request,'elegircuentaacrear.html')

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




# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.hashers import check_password  # Para comparar contraseñas cifradas
# from .models import Administrador  # Importa tu modelo Administrador

# def vista_inicioadmin(request):
#     if request.method == 'POST':
#         rut = request.POST.get('rut')
#         contrasena = request.POST.get('password')

#         # Validación del formato del RUT
#         if not validar_rut(rut):
#             messages.error(request, 'El RUT ingresado no es válido.')
#             return render(request, 'inicioAdmin.html')

#         try:
#             # Consulta para encontrar al administrador por RUT
#             admin = Administrador.objects.get(rut=rut)

#             # Verificar la contraseña
#             if check_password(contrasena, admin.contrasena):
#                 # Redirige al dashboard si es válido
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, 'La contraseña es incorrecta.')
#         except Administrador.DoesNotExist:
#             messages.error(request, 'El RUT ingresado no está registrado.')

#     return render(request, 'inicioAdmin.html')

# def validar_rut(rut):
#     """Valida el formato del RUT chileno. Ejemplo válido: 21270263-3"""
#     import re
#     pattern = r'^\d{1,8}-[0-9kK]$'
#     return re.match(pattern, rut) is not None


#-------------- Registrar Usuario ---------------------#
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Usuario

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Usuario  # Puedes dejar la importación de modelos fuera

# Generar un salt aleatorio
def generar_salt():
    return os.urandom(8).hex()


# Encriptar la contraseña usando el salt
def encriptar_con_salt(password, salt):
    password_bytes = (password + salt).encode('utf-8')
    return hashlib.sha256(password_bytes).hexdigest()


def registrar_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)

            # Generar un salt único
            salt = generar_salt()
            usuario.salt = salt

            # Encriptar la contraseña con el salt
            usuario.contrasena = encriptar_con_salt(form.cleaned_data["contrasena"], salt)

            # Poner el usuario como inactivo hasta que confirme
            usuario.is_active = False
            usuario.save()

            # Generar el token de activación
            uid = urlsafe_base64_encode(force_bytes(usuario.id))
            token = default_token_generator.make_token(usuario)

            # Crear enlace de activación
            activation_link = request.build_absolute_uri(
                reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
            )

            # Enviar el correo de activación
            email_subject = "Confirma tu cuenta en El Rincón de los Vecinos"
            email_body = render_to_string('email_confirmacion.html', {
                'nombre_usuario': usuario.nombre,
                'activation_link': activation_link
            })
            email = EmailMultiAlternatives(
                subject=email_subject,
                body=email_body,
                from_email="tuemail@gmail.com",  # Cambia por tu dirección
                to=[usuario.email],
            )
            email.attach_alternative(email_body, "text/html")
            email.send()

            messages.success(request, "Te hemos enviado un correo para confirmar tu cuenta. Revisa tu bandeja de entrada.")
            return redirect("catalogo")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
            messages.error(request, "Error en los datos ingresados. Revisa los campos.")
    else:
        form = UsuarioForm()
    return render(request, "registroUser.html", {"form": form})


def activar_cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(id=uid)
    except (Usuario.DoesNotExist, ValueError, TypeError):
        usuario = None

    if usuario and default_token_generator.check_token(usuario, token):
        usuario.is_active = True
        usuario.save()
        messages.success(request, "¡Tu cuenta ha sido activada con éxito! Ahora puedes iniciar sesión.")
        return redirect("iniciouser")
    else:
        messages.error(request, "El enlace de activación no es válido o ha expirado.")
        return render(request, "activation_invalid.html")

def validar_campo_unico(request):
    campo = request.GET.get("campo")
    valor = request.GET.get("valor")

    # Verificación para cada campo único
    if campo == "rut" and Usuario.objects.filter(rut=valor).exists():
        return JsonResponse({"existe": True, "mensaje": "Este RUT ya está registrado."})
    elif campo == "email" and Usuario.objects.filter(email=valor).exists():
        return JsonResponse({"existe": True, "mensaje": "Este correo electrónico ya está registrado."})
    elif campo == "telefono" and Usuario.objects.filter(telefono=valor).exists():
        return JsonResponse({"existe": True, "mensaje": "Este número de teléfono ya está registrado."})

    return JsonResponse({"existe": False})