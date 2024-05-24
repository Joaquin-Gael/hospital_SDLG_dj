from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_blog(request):
    return render(request, 'index.html',{'title':'Blog - Hospital SDLG'})

def atencion_al_paciente(request):
    return render(request, 'atencionalpaciente.html')

def contactos_blog(request):
    return render(request, 'contactos.html')