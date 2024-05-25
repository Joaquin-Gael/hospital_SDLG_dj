from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, dni, nombre, apellido, fecha_nacimiento, email, contraseña=None):
        if not dni:
            raise ValueError('El DNI es obligatorio')

        user = self.model(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            email=self.normalize_email(email),
        )

        user.set_password(contraseña)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, nombre, apellido, fecha_nacimiento, email, contraseña):
        user = self.create_user(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            email=email,
            contraseña=contraseña,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Create your models here.
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.especialidad}"

class Usuario(AbstractBaseUser):
    dni = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'fecha_nacimiento', 'email']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"Paciente: {self.usuario.nombre} {self.usuario.apellido}"

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_created = models.DateTimeField(auto_now=True)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return f"Turno de {self.paciente} con {self.medico} el {self.fecha}"
