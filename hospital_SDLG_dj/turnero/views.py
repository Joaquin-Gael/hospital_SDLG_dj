from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone
from . import models, forms

# Vista para mostrar el formulario de turno y procesar los datos enviados por el usuario.
@login_required
def form_turnero(request):
    """
    Esta vista maneja la presentación del formulario de turno y el procesamiento de los datos del formulario enviado por el usuario.
    Si la solicitud es un método POST, recopila los datos del formulario, crea un nuevo turno y lo guarda en la base de datos.
    Si el usuario no existe en la base de datos, muestra un mensaje de error.
    Devuelve una redirección a la página de inicio ('home_blog') después de crear el turno con éxito.
    """
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
        horario_turno = request.POST.get('horario')
        try:
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
        horario = models.Horario_medicos.objects.get(id=horario_turno)

        turno = models.Turno.objects.create(
            paciente=paciente,
            medico=medico,
            fecha=fecha_turno,
            motivo=motivo,
            horario=horario
        )

        messages.success(request, 'Turno creado exitosamente.')
        return redirect('home_blog')

    else:
        horarios = models.Horario_medicos.objects.all()
        medicos = models.Medico.objects.all()
        return render(request, 'formulario.html', {'medicos': medicos,'horarios':horarios})

# Vista para manejar el inicio de sesión del usuario.
def loguin_turnero(request):
    """
    Esta vista maneja el inicio de sesión del usuario.
    Si la solicitud es un método POST, intenta autenticar al usuario utilizando el DNI y la contraseña proporcionados.
    Si la autenticación es exitosa, inicia sesión en el sistema y redirige al usuario a la página de inicio ('home_blog').
    Si la autenticación falla, muestra un mensaje de error.
    Si la solicitud no es un método POST, simplemente muestra el formulario de inicio de sesión.
    """
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

# Vista para manejar el registro de un nuevo usuario.
def signup_turnero(request):
    """
    Esta vista maneja el proceso de registro de un nuevo usuario.
    Si la solicitud es un método POST y el formulario es válido, crea un nuevo usuario en la base de datos con la contraseña cifrada
    y lo redirige al formulario de turno.
    Si la solicitud no es un método POST, simplemente muestra el formulario de registro.
    """
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

# Vista para manejar el cierre de sesión del usuario.
def loguot_turnero(request):
    """
    Esta vista maneja el cierre de sesión del usuario.
    Simplemente cierra la sesión del usuario y redirige a la página de inicio ('home_blog').
    """
    logout(request)
    return redirect('home_blog')
