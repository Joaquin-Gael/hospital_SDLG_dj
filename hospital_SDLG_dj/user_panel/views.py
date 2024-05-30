from django.shortcuts import render, redirect
from turnero import models as turn_models
from django.contrib.auth.decorators import login_required

@login_required
def user_panel(request):
    """
    Vista para renderizar el panel de usuario.
    """
    return render(request, 'panel.html')

@login_required
def turnos_list(request):
    if request.method == 'POST':
        turno = request.POST.get('turno')
        print(turno)
        try:
            user = request.user
            try:
                paciente = turn_models.Paciente.objects.get(usuario=user)
                turn_models.Turno.eliminar_registros_antiguos()
                turno = turn_models.Turno.objects.get(id=turno)
                turno.delete()
                return redirect('lista_de_turnos')
            except Exception as err:
                print(err)
                turnos = []
                error_text = "Usted no tiene turnos"
                return render(request, 'turnos.html', {'turnos': turnos, 'error': error_text})
        except Exception as err:
            print(err)
            return redirect('home_blog')
    else:
        """
        Vista para listar los turnos del usuario.
        Si el usuario está autenticado, busca el paciente asociado a ese usuario y luego busca los turnos asociados a ese paciente.
        Si encuentra turnos, los muestra en una plantilla 'turnos.html'. Si no hay turnos, muestra un mensaje de error.
        Si el usuario no está autenticado o si ocurre algún error, redirige a la página de inicio ('home_blog').
        """
        try:
            user = request.user
            try:
                paciente = turn_models.Paciente.objects.get(usuario=user)
                turn_models.Turno.eliminar_registros_antiguos()
                turnos = turn_models.Turno.objects.filter(paciente=paciente)
                return render(request, 'turnos.html', {'turnos': turnos})
            except Exception as err:
                print(err)
                turnos = []
                error_text = "Usted no tiene turnos"
                return render(request, 'turnos.html', {'turnos': turnos, 'error': error_text})
        except Exception as err:
            print(err)
            return redirect('home_blog')
