
from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_catalogo, name='catalogo'), 
    path('registrouser/', views.vista_registrouser, name='registrouser'),
    path('iniciouser/', views.vista_iniciouser, name='iniciouser'),
    path('perfiluser/', views.vista_perfiluser, name='perfiluser'),
    path('historialuser/', views.vista_historialuser, name='historialuser'),

]