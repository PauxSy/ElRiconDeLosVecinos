from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    path('iniciouser/', views.vista_iniciouser, name='iniciouser'),
    path('recuperarcontrasena/', views.vista_recuperarcontrasena, name='recuperarcontrasena'),
    path('reset_password/<str:user_id>/', views.reset_password, name='reset_password'),

    # ---------------usuario----------------
    path('', views.vista_catalogo, name='catalogo'), 
    path('producto/<int:id>/', views.vista_detalleproducto, name='detalleproducto'),
    path('registrouser/', views.registrar_usuario, name='registrouser'),
    path("validar_campo_unico/", views.validar_campo_unico, name="validar_campo_unico"),
    path('carrito/', views.carrito, name='carrito'),  # Ruta para la vista de mostrar el carrito
    path('agregar_producto_carrito/<int:producto_id>/', views.agregar_producto_carrito, name='agregar_producto_carrito'),  # Ruta para agregar un producto al carrito
    path('carrito/', views.obtener_carrito, name='obtener_carrito'),
    path('perfiluser/', views.vista_perfiluser, name='perfiluser'),
    path('historialuser/', views.vista_historialuser, name='historialuser'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
    path('finalizarcompra/', views.finalizar_compra, name='finalizarcompra'),


    # ---------------Admin----------------
    path('reporteadmin/', views.vista_reporteadmin, name='reporteadmin'),
    path('agregarproducto/', views.vista_agregarproductoadmin, name='agregarproducto'),
    path('inventario/', views.vista_inventario, name='inventario'),
    #path('actualizarproducto/', views.vista_actualizarproducto, name='actualizarproducto'),
    path('deshabilitarproducto/', views.vista_deshabilitarproducto, name='deshabilitarproducto'),
    path('actualizarstock/', views.vista_actualizarstock, name='actualizarstock'),
    path('panelpromociones/', views.vista_panelpromociones, name='panelpromociones'),
    path('registroEmpleado/', views.vista_registroEmpleado, name='registroEmpleado'),
    path('dashboard/', views.vista_dashboard, name='dashboard'),

    path('perfiladmin/', views.vista_perfiladmin, name='perfiladmin'),
    
    path('guardar_productos/', views.guardar_productos, name='guardar_productos'),
    path('cambiar-imagen/<int:id>/', views.cambiar_imagen_producto, name='cambiar_imagen_producto'),
    path('generar_informe/', views.generar_informe_inventario, name='generar_informe'),


    # ---------------vendedor----------------
    path('ver_buscar_vendedor/', views.vista_ver_buscar_vendedor, name='ver_buscar_vendedor'),
    path('perfilvendedor/', views.vista_perfilvendedor, name='perfilvendedor'),

    path('panelvendedor/', views.vista_panelvendedor, name='panelvendedor'),

    # ---------------bodeguero----------------
    path('perfilbodeguero/', views.vista_perfilbodeguero, name='perfilbodeguero'),
  
    path('panelbodeguero/', views.vista_panelbodeguero, name='panelbodeguero'),

    # --------------vistas añadidas extras---------------

]

# Si usas archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
