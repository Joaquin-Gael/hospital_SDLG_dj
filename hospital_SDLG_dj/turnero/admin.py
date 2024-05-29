from django.contrib import admin
from .models import Especialidad, Medico, Paciente, Turno, Usuario, Horario_medicos

# Register your models here.

admin.site.register(Especialidad)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Turno)
admin.site.register(Usuario)
admin.site.register(Horario_medicos)