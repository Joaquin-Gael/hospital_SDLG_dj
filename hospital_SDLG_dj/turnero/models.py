from django.db import models

# Create your models here.
class Especialidad(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Medico(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)  # Fecha de registro del médico
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    turnos_reservados = models.ManyToManyField('Turno', related_name='usuarios')  # Relación con la tabla Turno

    def __str__(self):
        return self.nombre

class Turno(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    paciente = models.CharField(max_length=200)

    def __str__(self):
        return f'Turno para {self.paciente} con {self.medico.nombre} el {self.fecha_hora_inicio}'
