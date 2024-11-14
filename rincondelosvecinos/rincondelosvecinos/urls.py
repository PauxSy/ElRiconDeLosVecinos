
from django.urls import path
from . import views

urlpatterns = [
    # ---------------usuario----------------
    path('', views.vista_catalogo, name='catalogo'), 
    path('detalleproducto/', views.vista_detalleproducto, name='detalleproducto'),
    path('registrouser/', views.vista_registrouser, name='registrouser'),
    path('iniciouser/', views.vista_iniciouser, name='iniciouser'),
    path('perfiluser/', views.vista_perfiluser, name='perfiluser'),
    path('historialuser/', views.vista_historialuser, name='historialuser'),

    path('detalleproducto2/<int:id>/', views.vista_detalleproducto2, name='detalleproducto2'), #prueba base de datos


    # ---------------Admin----------------
    path('inicioadmin/', views.vista_inicioadmin, name='inicioadmin'),
    path('reporteadmin/', views.vista_reporteadmin, name='reporteadmin'),
    path('agregarproducto/', views.vista_agregarproductoadmin, name='agregarproducto'),
    path('inventario/', views.vista_inventario, name='inventario'),
    path('actualizarproducto/', views.vista_actualizarproducto, name='actualizarproducto'),
    path('deshabilitarproducto/', views.vista_deshabilitarproducto, name='deshabilitarproducto'),
    path('actualizarstock/', views.vista_actualizarstock, name='actualizarstock'),
    
    path('panelpromociones/', views.vista_panelpromociones, name='panelpromociones'),

    path('registrovendedor/', views.vista_registrovendedor, name='registrovendedor'),
    path('registrobodeguero/', views.vista_registrobodeguero, name='registrobodeguero'),
    path('dashboard/', views.vista_dashboard, name='dashboard'),

    # ---------------venderor----------------
    path('iniciovendedor/', views.vista_iniciovendedor, name='iniciovendedor'),
    path('panelvendedor/', views.vista_panelvendedor, name='panelvendedor'),

    # ---------------bodeguero----------------
    path('iniciobodeguero/', views.vista_iniciobodeguero, name='iniciobodeguero'),
    path('panelbodeguero/', views.vista_panelbodeguero, name='panelbodeguero'),

    #--------------vistas_añadidas_extras_---------------
    path('seleccionarcuentainicio/', views.vista_seleccionarcuentainicio, name='seleccionarcuentainicio'),
    path('elegircuentaacrear/', views.vista_elegircuentaacrear, name='elegircuentaacrear'),

]