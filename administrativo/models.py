from django.db import models
from django.utils.translation import gettext_lazy as _


class AWS_CREDENCIALES(models.Model):
    AWS_ACCESS_KEY_ID = models.CharField(max_length=150)
    AWS_SECRET_ACCESS_KEY = models.CharField(max_length=150)
    AWS_STORAGE_BUCKET_NAME = models.CharField(max_length=150)
    AWS_REGION = models.CharField(max_length=150)
    IMAGEN_BASE_URL = models.CharField(max_length=150)
    VIDEO_BASE_URL = models.CharField(max_length=150)
    FECHA_INGRESO_AWS = models.DateTimeField(auto_now_add=True)
    FECHA_MODIFICACION_AWS = models.DateField(auto_now=True)
    ESTADO_AWS = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Credencial AWS")
        verbose_name_plural = _("Credenciales AWS")

    def __str__(self):
        return self.AWS_STORAGE_BUCKET_NAME

class BOT_CREDENCIALES(models.Model):
    PRIVATE_KEY_BOT_CREDENCIAL = models.CharField(max_length=255)
    NOMBRE_BOT_CREDENCIALES = models.CharField(max_length=255)
    FECHA_INGRESO_BOT_CREDENCIALES = models.DateTimeField(auto_now_add=True)
    FECHA_MODIFICACION_BOT_CREDENCIALES = models.DateField(auto_now=True)
    ESTADO_BOT_CREDENCIALES = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Credencial de bot")
        verbose_name_plural = _("Credenciales de bots")

    def __str__(self):
        return self.NOMBRE_BOT_CREDENCIALES
