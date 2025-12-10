from django.db import models
from django.db.models import BooleanField
from django.utils.translation import gettext_lazy as _
from general.models import USUARIO
##############################################################################
class CURSO(models.Model):
    NOMBRE_CURSO = models.CharField(max_length=255)
    DESCRIPCION_CURSO = models.CharField(max_length=255)
    URL_PORTADA_CURSO = models.CharField(max_length=255, null=True, blank=True)
    PUNTUACION_GENERAL_CURSO = models.DecimalField(max_digits=4, decimal_places=2)
    SUBSCRIPCION_TOTAL_CURSO = models.IntegerField()
    DURACION_TOTAL_CURSO = models.DecimalField(max_digits=6, decimal_places=2)
    COSTO_TOTAL_CURSO = models.DecimalField(max_digits=6, decimal_places=2)
    ITEM_TOTAL_CURSO = models.IntegerField()
    FECHA_MODIFICACION_CURSO = models.DateField(auto_now=True)
    FECHA_INGRESO_CURSO = models.DateTimeField(auto_now_add=True)
    ESTADO_CURSO = models.BooleanField(default=True)
    ESTADO_PUBLICACION_CURSO = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")

    def __str__(self):
        return self.NOMBRE_CURSO

class REQUISITO(models.Model):
    curso = models.ForeignKey(CURSO, on_delete=models.CASCADE, related_name="requisitos")

    NOMBRE_REQUISITO = models.CharField(max_length=150)
    FECHA_MODIFICACION_REQUISITO = models.DateField(auto_now=True)
    FECHA_INGRESO_REQUISITO = models.DateTimeField(auto_now_add=True)
    ESTADO_REQUISITO = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Requisito")
        verbose_name_plural = _("Requisitos")

    def __str__(self):
        return self.NOMBRE_REQUISITO

class POLITICA(models.Model):
    curso = models.ForeignKey(CURSO, on_delete=models.CASCADE, related_name="politicas")
    NOMBRE_POLITICA = models.CharField(max_length=255)
    DESCRIPCION_POLITICA = models.CharField(max_length=255)
    FECHA_MODIFICACION_POLITICA = models.DateField(auto_now=True)
    FECHA_INGRESO_POLITICA = models.DateTimeField(auto_now_add=True)
    ESTADO_POLITICA = models.BooleanField(default=True)


    class Meta:
        verbose_name = _("Politica")
        verbose_name_plural = _("Politicas")

    def __str__(self):
        return self.NOMBRE_POLITICA

class ACTXCUR(models.Model):
    curso = models.ForeignKey(CURSO, on_delete=models.CASCADE, related_name="secciones")
    ORDEN_SECCION_CURSO = models.IntegerField()
    NOMBRE_ACTXCUR = models.CharField(max_length=255, blank=True)
    FECHA_MODIFICACION_ACTXCUR = models.DateField(auto_now=True)
    FECHA_INGRESO_ACTXCUR = models.DateTimeField(auto_now_add=True)
    ESTADO_ACTXCUR = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Sección de curso")
        verbose_name_plural = _("Secciones de curso")
        ordering = ["ORDEN_SECCION_CURSO"]

    def __str__(self):
        return f"Sección {self.ORDEN_SECCION_CURSO} - {self.curso}"

class TIPO_ACTIVIDAD(models.Model):
    NOMBRE_TIPO_ACTIVIDAD = models.CharField(max_length=255)
    FECHA_MODIFICACION_TIPO_ACTIVIDAD = models.DateField(auto_now=True)
    FECHA_INGRESO_TIPO_ACTIVIDAD = models.DateTimeField(auto_now_add=True)
    ESTADO_TIPO_ACTIVIDAD = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Tipo de actividad")
        verbose_name_plural = _("Tipos de actividad")

    def __str__(self):
        return self.NOMBRE_TIPO_ACTIVIDAD

class ACTIVIDAD(models.Model):
    tipo_actividad = models.ForeignKey(
        TIPO_ACTIVIDAD,
        on_delete=models.CASCADE,
        related_name="actividades"
    )

    seccion = models.ForeignKey(
        ACTXCUR,
        on_delete=models.CASCADE,
        related_name="actividades"
    )

    NOMBRE_ACTIVIDAD = models.CharField(max_length=255)
    DURACION_TOTAL_ACTIVIDAD = models.DecimalField(max_digits=8, decimal_places=2)

    FECHA_MODIFICACION_ACTIVIDAD = models.DateField(auto_now=True)
    FECHA_INGRESO_ACTIVIDAD = models.DateTimeField(auto_now_add=True)
    ESTADO_ACTIVIDAD = models.BooleanField(default=True)
    PUNTUACION_GENERAL_ACTIVIDAD = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Actividad")
        verbose_name_plural = _("Actividades")

    def __str__(self):
        return self.NOMBRE_ACTIVIDAD

class VIDEO_ACTIVIDAD(models.Model):
    actividad = models.ForeignKey(ACTIVIDAD, on_delete=models.CASCADE, related_name="videos")

    URL_VIDEO_ACTIVIDAD = models.CharField(max_length=255)
    FECHA_MODIFICACION_VIDEO_ACTIVIDAD = models.DateField(auto_now=True)
    FECHA_INGRESO_VIDEO_ACTIVIDAD = models.DateTimeField(auto_now_add=True)
    ESTADO_VIDEO_ACTIVIDAD = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Video de actividad")
        verbose_name_plural = _("Videos de actividad")

    def __str__(self):
        return self.URL_VIDEO_ACTIVIDAD

class IMAGEN_ACTIVIDAD(models.Model):
    actividad = models.ForeignKey(ACTIVIDAD, on_delete=models.CASCADE, related_name="imagenes")

    URL_IMAGEN_ACTIVIDAD = models.CharField(max_length=255)
    FECHA_MODIFICACION_IMAGEN_ACTIVIDAD = models.DateField(auto_now=True)
    FECHA_INGRESO_IMAGEN_ACTIVIDAD = models.DateTimeField(auto_now_add=True)
    ESTADO_IMAGEN_ACTIVIDAD = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Imagen de actividad")
        verbose_name_plural = _("Imágenes de actividad")

    def __str__(self):
        return self.URL_IMAGEN_ACTIVIDAD

class DESCRIPCION_ACTIVIDAD(models.Model):
    actividad = models.ForeignKey(ACTIVIDAD, on_delete=models.CASCADE, related_name="descripciones")

    DESCRIPCION_DESCRIPCION_ACTIVIDAD = models.CharField(max_length=255)
    FECHA_MODIFICACION_DESCRIPCION_ACTIVIDAD = models.DateField(auto_now=True)
    FECHA_INGRESO_DESCRIPCION_ACTIVIDAD = models.DateTimeField(auto_now_add=True)
    ESTADO_DESCRIPCION_ACTIVIDAD = models.BooleanField(default=True)
    ORDEN_DESCRIPCION = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _("Descripción de actividad")
        verbose_name_plural = _("Descripciones de actividad")

    def __str__(self):
        return self.DESCRIPCION_DESCRIPCION_ACTIVIDAD

class FORO(models.Model):
    actividad = models.ForeignKey(ACTIVIDAD, on_delete=models.CASCADE, null=True, blank=True)

    NOMBRE_FORO = models.CharField(max_length=255)
    DESCRIPCION_FORO = models.CharField(max_length=255)

    FECHA_INGRESO_FORO = models.DateTimeField(auto_now_add=True)
    FECHA_MODIFICACION_FORO = models.DateField(auto_now=True)
    ESTADO_FORO = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Foro")
        verbose_name_plural = _("Foros")

    def __str__(self):
        return self.NOMBRE_FORO

class PDF_ACTIVIDAD(models.Model):

    actividad = models.ForeignKey(
        ACTIVIDAD,
        on_delete=models.CASCADE,
        related_name="pdfs"
    )

    URL_PDF_ACTIVIDAD = models.CharField(
        max_length=255,
        verbose_name="URL del PDF"
    )
    FECHA_INGRESO_PDF_ACTIVIDAD = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de subida"
    )
    FECHA_MODIFICACION_PDF_ACTIVIDAD = models.DateField(auto_now=True)

    ESTADO_PDF_ACTIVIDAD = models.BooleanField(
        default=True,
        verbose_name="PDF activo"
    )

    class Meta:
        verbose_name = "PDF de actividad"
        verbose_name_plural = "PDF de actividades"

    def __str__(self):
        return f"PDF - {self.actividad.NOMBRE_ACTIVIDAD}"

class ACTXUSE(models.Model):
    usuario = models.ForeignKey(USUARIO, on_delete=models.CASCADE)
    actividad = models.ForeignKey(
        ACTIVIDAD,
        on_delete=models.CASCADE,
        related_name="actividades_por_usuario"
    )
    COMPLETO_ACTXUSE = models.BooleanField(default=False)
    ESTADO_ACTXUSE = models.BooleanField(default=True)
    FECHA_INGRESO_ACTXUSE = models.DateTimeField(auto_now_add=True)
    FECHA_MODIFICACION_ACTXUSE = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'actividad')


##############################################################################
class OPINION_ACTIVIDAD(models.Model):
    usuario = models.ForeignKey(
        USUARIO,
        on_delete=models.CASCADE,
        related_name="opiniones"
    )

    actividad = models.ForeignKey(
        ACTIVIDAD,
        on_delete=models.CASCADE,
        related_name="opiniones"
    )

    DESCRIPCION_OPINION_ACTIVIDAD = models.CharField(max_length=255)
    PUNTUACION_OPINION_ACTIVIDAD = models.DecimalField(max_digits=4, decimal_places=2)
    # FALTA LA AUTORELACION
    FECHA_MODIFICACION_OPINION_ACTIVIDAD = models.DateField(auto_now=True)
    FECHA_INGRESO_OPINION_ACTIVIDAD = models.DateTimeField(auto_now_add=True)
    ESTADO_OPINION_ACTIVIDAD = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Opinión de actividad")
        verbose_name_plural = _("Opiniones de actividad")

    def __str__(self):
        return f"{self.usuario} → {self.actividad}"

class OPINION_FORO(models.Model):
    usuario = models.ForeignKey(
        USUARIO,
        on_delete=models.CASCADE,
        related_name="opiniones_foro"
    )

    foro = models.ForeignKey(
        FORO,
        on_delete=models.CASCADE,
        related_name="opiniones"
    )
    OPINION_OPINION_FORO = models.CharField(max_length=255, null=True, blank=True)
    FECHA_INGRESO_OPINION_FORO = models.DateTimeField(auto_now_add=True)
    FECHA_MODIFICACION_OPINION_FORO = models.DateField(auto_now=True)
    ESTADO_OPINION_FORO = models.BooleanField(default=True)
    # FALTA LA AUTORELACION

    class Meta:
        verbose_name = _("Opinión de foro")
        verbose_name_plural = _("Opiniones de foro")

    def __str__(self):
        return f"{self.usuario} → {self.foro}"

##############################################################################
##############################################################################
class CURXUSE(models.Model):
    usuario = models.ForeignKey(USUARIO, on_delete=models.CASCADE)
    curso = models.ForeignKey(CURSO, on_delete=models.CASCADE)
    FECHA_MODIFICACION_CURXUSE = models.DateField(auto_now=True)
    FECHA_INGRESO_CURXUSE = models.DateTimeField(auto_now_add=True)
    ESTADO_CURXUSE = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Curso por usuario")
        verbose_name_plural = _("Cursos por usuario")
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'curso'], name='unique_usuario_curso')
        ]

    def __str__(self):
        return f"{self.usuario} → {self.curso}"
##############################################################################