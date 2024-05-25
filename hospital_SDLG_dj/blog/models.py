from django.db import models
from turnero import models as turnero_models

# Create your models here.

class Testimonios(models.Model):
    contenido = models.TextField()
    usuario = models.ForeignKey(turnero_models.Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Testimonio del usuario: {self.usuario}"