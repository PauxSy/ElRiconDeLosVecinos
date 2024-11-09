from django.shortcuts import render

def vista_catalogo(request):
    return render(request, 'catalogo.html')

def vista_iniciouser(request):
    return render(request, 'inicioSesioónUser.html')
