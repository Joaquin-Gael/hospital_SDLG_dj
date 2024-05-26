from django.urls import path
from . import views

urlpatterns = [
    path('panel/',views.user_panel)
]