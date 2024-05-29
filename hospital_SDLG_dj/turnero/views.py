from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone
from . import models, forms

# Create your views here.
@login_required
def form_turnero(request):
    if request.method == 'POST':
        paciente_nombre = request.POST.get('paciente_nombre')
        paciente_apellido = request.POST.get('paciente_apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        medico_id = request.POST.get('medico')
        fecha_turno = request.POST.get('fecha')
        motivo = request.POST.get('motivo')
        horario_turno = request.POST.grt('horario')
        try:
            print(horario_turno)
            usuario = models.Usuario.objects.get(
                nombre=paciente_nombre,
                apellido=paciente_apellido,
                fecha_nacimiento=fecha_nacimiento,
                email=email
            )
        except models.Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado. Por favor, registre el usuario primero.')
            medicos = models.Medico.objects.all()
            return render(request, 'formulario.html', {'medicos': medicos, 'error':'No se encontro usuario existente con esta descripcion\n le recomiendo que se registre'})

        paciente, created = models.Paciente.objects.get_or_create(
            usuario=usuario,
            defaults={'direccion': direccion, 'telefono': telefono}
        )

        medico = models.Medico.objects.get(id=medico_id)

        turno = models.Turno.objects.create(
            paciente=paciente,
            medico=medico,
            fecha=fecha_turno,
            motivo=motivo,
            horario=horario_turno
        )

        messages.success(request, 'Turno creado exitosamente.')
        return redirect('home_blog')

    else:
        horarios = models.Horario_medicos.objects.all()
        medicos = models.Medico.objects.all()
        return render(request, 'formulario.html', {'medicos': medicos,'horarios':horarios})

def loguin_turnero(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        password = request.POST.get('password')

        # Autenticar al usuario utilizando el DNI
        user = authenticate(request, dni=dni, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_blog') 
        else:
            return render(request, 'Login.html', {'error': 'Invalid credentials'})
    return render(request, 'Login.html')

def signup_turnero(request):
    if request.method == 'POST':
        form = forms.RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['contraseña'])
            usuario.save()
            return redirect('form_turnero')
    else:
        form = forms.RegistroUsuarioForm() 
    return render(request, 'SignUp.html')