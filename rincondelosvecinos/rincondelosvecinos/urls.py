
from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_catalogo, name='catalogo'),  
    path('iniciouser/', views.vista_iniciouser, name='iniciouser'), 
]