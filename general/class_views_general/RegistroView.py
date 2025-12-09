from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from general.models import USUARIO


class RegistroView(View):
    template_name = 'general/register/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        data = request.POST

        # Obtener campos
        primer_nombre = data.get("primer_nombre")
        segundo_nombre = data.get("segundo_nombre")
        primer_apellido = data.get("primer_apellido")
        segundo_apellido = data.get("segundo_apellido")
        apodo = data.get("apodo")
        correo = data.get("email")
        telefono = data.get("telefono")
        fecha_nacimiento = data.get("fecha_nacimiento")
        direccion = data.get("direccion")
        password = data.get("password")
        password2 = data.get("password2")

        # Validar contraseñas
        if password != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("registro")

        # Validar correo único
        if USUARIO.objects.filter(CORREO_USUARIO=correo).exists():
            messages.error(request, "Este correo ya está registrado")
            return redirect("registro")

        # Crear usuario
        user = USUARIO.objects.create_user(
            correo,  # primer argumento posicional
            password,  # segundo posicional
            PRIMER_NOMBRE_USUARIO=primer_nombre,
            SEGUNDO_NOMBRE_USUARIO=segundo_nombre,
            PRIMER_APELLIDO_USUARIO=primer_apellido,
            SEGUNDO_APELLIDO_USUARIO=segundo_apellido,
            APODO=apodo,
            TELEFONO_USUARIO=telefono,
            FECHA_NACIMIENTO_USUARIO=fecha_nacimiento,
            DIRECCION_USUARIO=direccion,
        )

        messages.success(request, "Cuenta creada correctamente")
        return redirect("login")
