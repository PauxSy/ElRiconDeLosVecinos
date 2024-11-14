from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
#----------------------------------------------------------------
#PRUEBA PARA VER SI CONECTA CON LA BD
from django.http import JsonResponse
from .models import Producto
def vista_detalleproducto(request, id):
    # Obtén el producto con el id proporcionado en la URL
    producto = get_object_or_404(Producto, id=id)
    
    # Pasa el producto a la plantilla
    return render(request, 'detalleProducto.html', {'producto': producto})
# ---------------usuario----------------

def vista_catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo.html', {'productos': productos})



def vista_registrouser(request):
    return render(request,'registroUser.html')

def vista_iniciouser(request):
    return render(request, 'inicioSesioónUser.html')

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



