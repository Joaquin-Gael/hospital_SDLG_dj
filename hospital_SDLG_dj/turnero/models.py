from django.db import models

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
        return f"{self.nombre} {self.apellido}"

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    email = models.EmailField()
    contraseña = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Paciente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"Paciente: {self.usuario.nombre} {self.usuario.apellido}"

class Turno(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return f"Turno de {self.paciente} con {self.medico} el {self.fecha}"
