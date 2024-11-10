from django.shortcuts import render

# ---------------usuario---------------- 

def vista_catalogo(request):
    return render(request, 'catalogo.html')

def vista_registrouser(request):
    return render(request,'registroUser.html')

def vista_iniciouser(request):
    return render(request, 'inicioSesioónUser.html')

def vista_perfiluser(request):
    return render(request,'perfilUser.html')

def vista_historialuser(request):
    return render(request,'historialCompraUser.html')


# ---------------Admin---------------- 

def vista_



