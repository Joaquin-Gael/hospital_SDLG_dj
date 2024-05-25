from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from . import models, forms

# Create your views here.
@login_required
def form_turnero(request):
    if request.method == 'POST':
        print(request.POST)
        form = forms.TurnoForm(request.POST)
        if form.is_valid():
            try:
                usuario = models.Usuario.objects.get(
                    nombre=form.cleaned_data['paciente_nombre'],
                    apellido=form.cleaned_data['paciente_apellido'],
                    fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                    email=form.cleaned_data['email']
                )
            except models.Usuario.DoesNotExist:
                return redirect('registro_usuario')
            paciente, created = models.Paciente.objects.get_or_create(
                usuario=usuario,
                defaults={'direccion': form.cleaned_data['direccion']}
            )
            turno = form.save(commit=False)
            turno.paciente = paciente
            turno.save()
            return redirect('home_blog')
        else:
            medicos = models.Medico.objects.all()
            return render(request, 'formulario.html',{'medicos':medicos})
    else:
        form = forms.TurnoForm()
    medicos = models.Medico.objects.all()
    return render(request, 'formulario.html',{'medicos':medicos})

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
    return render(request, 'SignUp.html', {'form': form})