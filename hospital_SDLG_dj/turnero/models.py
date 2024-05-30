from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from datetime import time, timedelta

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

class Horario_medicos(models.Model):
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self) -> str:
        return f"{self.medico} {self.hora_inicio} {self.hora_fin}"

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
        return f"{self.nombre} {self.apellido} {self.fecha_nacimiento}"

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
    telefono = models.CharField(max_length=255)

    def __str__(self):
        return f"Paciente: {self.usuario.nombre} {self.usuario.apellido}"

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_created = models.DateTimeField(auto_now=True)
    fecha = models.DateField(default=timezone.now)
    horario = models.ForeignKey(Horario_medicos,on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255)

    @classmethod
    def eliminar_registros_antiguos(cls, dias=0):
        """
        Método de clase para eliminar registros creados en la fecha y hora actual o en los últimos días especificados.
        :param dias: Número de días antes de la fecha y hora actual para incluir en la eliminación.
        """
        fecha_actual = timezone.now()
        fecha_limite = fecha_actual - timedelta(days=dias)
        registros_actuales = cls.objects.filter(fecha_created__date=fecha_actual.date(), fecha_created__time=fecha_actual.time())
        if dias > 0:
            registros_actuales = registros_actuales.filter(fecha_created__gte=fecha_limite)
        registros_actuales.delete()
    
    def __str__(self):
        return f"Turno de {self.paciente} con {self.medico} el {self.fecha}"
