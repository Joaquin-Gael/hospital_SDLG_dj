from django.contrib.auth.backends import BaseBackend
from .models import Usuario

class DNIAuthBackend(BaseBackend):
    def authenticate(self, request, dni=None, password=None):
        try:
            usuario = Usuario.objects.get(dni=dni)
            if usuario.check_password(password):
                return usuario
        except Usuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
