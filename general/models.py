from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    """Manager personalizado para el modelo USUARIO."""

    use_in_migrations = True

    def create_user(self, correo_usuario, password=None, **extra_fields):
        """Crea y guarda un usuario normal."""
        if not correo_usuario:
            raise ValueError(_("El correo electrónico es obligatorio"))

        correo_usuario = self.normalize_email(correo_usuario)

        # Por si no te pasan estos flags
        extra_fields.setdefault("IS_ACTIVE", True)
        extra_fields.setdefault("IS_STAFF", False)

        user = self.model(
            CORREO_USUARIO=correo_usuario,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_usuario, password=None, **extra_fields):
        """Crea y guarda un superusuario."""
        extra_fields.setdefault("IS_STAFF", True)
        extra_fields.setdefault("IS_SUPERUSER", True)
        extra_fields.setdefault("IS_ACTIVE", True)

        if extra_fields.get("IS_STAFF") is not True:
            raise ValueError(_("El superusuario debe tener IS_STAFF=True."))
        if extra_fields.get("IS_SUPERUSER") is not True:
            raise ValueError(_("El superusuario debe tener IS_SUPERUSER=True."))

        return self.create_user(correo_usuario, password, **extra_fields)

class USUARIO(AbstractBaseUser, PermissionsMixin):
    ID = models.AutoField(primary_key=True)
    ID_CIUDAD = models.IntegerField(null=True, blank=True)
    APODO = models.CharField(max_length=150)
    PRIMER_NOMBRE_USUARIO = models.CharField(max_length=150)
    SEGUNDO_NOMBRE_USUARIO = models.CharField(max_length=150, blank=True)
    PRIMER_APELLIDO_USUARIO = models.CharField(max_length=150)
    SEGUNDO_APELLIDO_USUARIO = models.CharField(max_length=150, blank=True)

    TELEFONO_USUARIO = models.CharField(max_length=150)
    DIRECCION_USUARIO = models.CharField(max_length=150)
    FECHA_NACIMIENTO_USUARIO = models.DateField()

    CORREO_USUARIO = models.EmailField(unique=True)

    IS_STAFF = models.BooleanField(default=False)
    IS_ACTIVE = models.BooleanField(default=True)
    DATE_JOINED = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'CORREO_USUARIO'
    REQUIRED_FIELDS = ['PRIMER_NOMBRE_USUARIO', 'PRIMER_APELLIDO_USUARIO', 'APODO']

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")

    def __str__(self):
        return f"{self.PRIMER_NOMBRE_USUARIO} {self.PRIMER_APELLIDO_USUARIO}"

class AVATAR(models.Model):
    usuario = models.OneToOneField(USUARIO, on_delete=models.CASCADE, related_name="avatar")

    URL_AVATAR_USER = models.CharField(max_length=250)
    FECHA_MODIFICACION_AVATAR = models.DateField(auto_now=True)
    FECHA_INGRESO_AVATAR = models.DateTimeField(auto_now_add=True)
    ESTADO_AVATAR = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Avatar")
        verbose_name_plural = _("Avatares")

    def __str__(self):
        return f"Avatar de {self.usuario}"
