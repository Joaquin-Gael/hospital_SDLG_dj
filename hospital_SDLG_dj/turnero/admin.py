from django.contrib import admin
from .models import Especialidad, Medico, Paciente, Turno, Usuario

# Register your models here.

admin.site.register(Especialidad)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(Turno)
admin.site.register(Usuario)