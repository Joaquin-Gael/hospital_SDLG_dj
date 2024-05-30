from django.urls import path
from . import views

urlpatterns = [
    path('form/',views.form_turnero,name='turnero'),
    path('login/',views.loguin_turnero,name='form_turnero'),
    path('singup/',views.signup_turnero,name='registro_usuario'),
    path('loguot/',views.loguot_turnero,name='loguot_turnero')
]