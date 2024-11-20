from django.shortcuts import get_object_or_404, render #PRUEBA PARA VER SI CONECTA CON LA BD
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from .models import Producto , Usuario,Administrador
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse


from datetime import datetime, timedelta

def vista_iniciouser(request):
    # Verificar si ya hay una sesión activa
    if request.session.get('nombre_usuario') and request.session.get('primer_apellido'):
        messages.error(request, "Ya tienes una sesión iniciada. Por favor, cierra sesión antes de intentar iniciar una nueva sesión.")
        return redirect('catalogo')

    # Número máximo de intentos permitidos y tiempo de bloqueo (en minutos)
    LIMITE_INTENTOS = 2
    TIEMPO_BLOQUEO = 1  # En minutos

    # Inicializar el contador de intentos fallidos y el tiempo de bloqueo si no existen
    if 'login_attempts' not in request.session:
        request.session['login_attempts'] = 0
    if 'bloqueado_hasta' not in request.session:
        request.session['bloqueado_hasta'] = None

    # Verificar si el usuario está bloqueado
    bloqueado_hasta = request.session.get('bloqueado_hasta')
    if bloqueado_hasta:
        # Convertir el tiempo de bloqueo a objeto datetime
        bloqueado_hasta = datetime.strptime(bloqueado_hasta, '%Y-%m-%d %H:%M:%S')
        if datetime.now() < bloqueado_hasta:
            tiempo_restante = (bloqueado_hasta - datetime.now()).seconds // 60
            messages.error(request, f"Has sido bloqueado temporalmente. Intenta de nuevo en {tiempo_restante} minutos.")
            return render(request, 'inicioSesioónUser.html')
        else:
            # Desbloquear al usuario si el tiempo ha pasado
            request.session['bloqueado_hasta'] = None
            request.session['login_attempts'] = 0

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Busca el usuario en la base de datos
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.contrasena == password:
                # Inicio de sesión exitoso
                # Reiniciar el contador de intentos fallidos y desbloquear
                request.session['login_attempts'] = 0
                request.session['bloqueado_hasta'] = None

                # Guardar datos del usuario en la sesión
                request.session['nombre_usuario'] = usuario.nombre
                request.session['primer_apellido'] = usuario.primer_apellido

                messages.success(request, "Inicio de sesión exitoso")
                return redirect('catalogo')
            else:
                # Incrementar el contador de intentos fallidos
                request.session['login_attempts'] += 1
                messages.error(request, "Contraseña incorrecta")
        except Usuario.DoesNotExist:
            # Incrementar el contador de intentos fallidos
            request.session['login_attempts'] += 1
            messages.error(request, "El email no está registrado")

        # Bloquear al usuario si supera el límite de intentos
        if request.session['login_attempts'] >= LIMITE_INTENTOS:
            bloqueado_hasta = datetime.now() + timedelta(minutes=TIEMPO_BLOQUEO)
            request.session['bloqueado_hasta'] = bloqueado_hasta.strftime('%Y-%m-%d %H:%M:%S')
            messages.error(request, f"Has superado el número de intentos permitidos. Estarás bloqueado durante {TIEMPO_BLOQUEO} minutos.")

    return render(request, 'inicioSesioónUser.html')



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

#     return render(request, 'inicioSesioónUser.html')



def vista_recuperarcontraseña(request):
    # Validar si ya hay una sesión activa
    if request.session.get('nombre_usuario') and request.session.get('primer_apellido'):
        messages.error(request, "Ya tienes una sesión iniciada. Por favor, cierra sesión antes de recuperar la contraseña.")
        return redirect('catalogo')  # Redirigir al catálogo u otra página adecuada

    if request.method == "POST":
        email = request.POST.get('email')

        # Validar si el correo existe en la base de datos de Usuario o Administrador
        usuario = Usuario.objects.filter(email=email).first()
        administrador = Administrador.objects.filter(email=email).first()

        if not usuario and not administrador:
            messages.error(request, "No existe un usuario registrado con ese correo.")
            return render(request, 'recuperarcontraseña.html')

        # Seleccionar el usuario o administrador y generar un enlace diferenciado
        if usuario:
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[f"usuario_{usuario.id}"]))
        else:
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[f"admin_{administrador.id}"]))

        # Enviar el correo con el enlace de recuperación
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

    return render(request, "recuperarcontraseña.html")


def reset_password(request, user_id):
    if request.method == "POST":
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        # Validar si las contraseñas coinciden
        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
            return render(request, 'reset_password.html', {'user_id': user_id})

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
            return render(request, 'reset_password.html', {'user_id': user_id})

        # Actualizar la contraseña
        usuario_obj.contrasena = nueva_contrasena  # Guardar la contraseña sin encriptar
        usuario_obj.save()

        messages.success(request, "Tu contraseña ha sido actualizada con éxito.")
        return redirect('catalogo')

    # Renderizar la plantilla con el ID en el contexto
    return render(request, 'reset_password.html', {'user_id': user_id})






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
    return render(request, 'catalogo.html', {'productos': productos, 'query': query})

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
    return render(request,'perfilUser.html')

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

def registrar_usuario(request):
    from .forms import UsuarioForm  # Mueve la importación aquí para evitar el conflicto
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.contrasena = make_password(form.cleaned_data["contrasena"])
            usuario.save()
            messages.success(request, "Usuario registrado exitosamente.")
            return redirect("catalogo")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
            messages.error(request, "Error en los datos ingresados. Revisa los campos.")
    else:
        form = UsuarioForm()
    return render(request, "registroUser.html", {"form": form})

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