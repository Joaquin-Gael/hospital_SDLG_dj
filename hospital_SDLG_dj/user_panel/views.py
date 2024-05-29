from django.shortcuts import render, redirect
from turnero import models as turn_models
from django.contrib.auth.decorators import login_required

# Create your views here.
def user_panel(request):
    return render(request,'panel.html')

@login_required
def turnos_list(request):
    try:
        user = request.user
        try:
            paciente = turn_models.Paciente.objects.get(usuario=user)
            turnos = turn_models.Turno.objects.filter(paciente=paciente)
            return render(request,'turnos.html',{'turnos':turnos})
        except Exception as err:
            print(err)
            turnos = []
            error_text = "Usted no tiene turnos"
            return render(request,'turnos.html',{'turnos':turnos,'error':error_text})
    except Exception as err:
        print(err)
        return redirect('home_blog')