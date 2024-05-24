from django.urls import path
from . import views

urlpatterns = [
    path('form/',views.form_turnero),
    path('loguin/',views.loguin_turnero),
    path('singup/',views.signup_turnero)
]