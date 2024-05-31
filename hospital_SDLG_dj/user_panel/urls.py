from django.urls import path
from . import views

urlpatterns = [
    path('panel/',views.user_panel,name='panel'),
    path('turnos/',views.turnos_list,name='lista_de_turnos'),
    path('testimonios/',views.form_testimonios,name='testimonios_form')
]