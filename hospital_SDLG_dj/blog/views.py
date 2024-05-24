from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_blog(request):
    return render(request, 'index.html',{'title':'home_blog'})

def atencion_al_paciente(request):
    return render(request, 'atencionalpaciente.html',{'title':'atencion al cliente'})

def contactos_blog(request):
    return render(request, 'contactos.html',{'title':'contactos'})