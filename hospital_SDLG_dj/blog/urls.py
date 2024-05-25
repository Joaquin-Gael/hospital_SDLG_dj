from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_blog, name='home_blog'),
    path('atencion_al_paciente/',views.atencion_al_paciente, name='atencion_blog'),
    path('contactos/',views.contactos_blog)
]
