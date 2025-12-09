from django.views.generic import TemplateView
import openai
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from cursos.models import CURSO, CURXUSE
from cursos.models import REQUISITO, POLITICA, ACTXCUR, ACTIVIDAD
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from cursos.models import CURSO, ACTXCUR, ACTIVIDAD, CURXUSE
from django.db import connection
import json
from django.db.models import Avg
from django.db.models import Avg
from cursos.models import (
    ACTIVIDAD, VIDEO_ACTIVIDAD, PDF_ACTIVIDAD, IMAGEN_ACTIVIDAD,
    DESCRIPCION_ACTIVIDAD, OPINION_ACTIVIDAD, ACTXUSE, FORO
)

class CursosView(TemplateView):
    template_name = 'cursos/catalogo/index.html'

    extra_context = {
        'titulo_pagina': 'ChugChillian — Cursos Comunitarios'
    }


class CursosViewAjax(View):
    def get(self, request):
        cursos_bd = CURSO.objects.filter(ESTADO_CURSO=True)

        cursos = []

        for curso in cursos_bd:
            cursos.append({
                'id': curso.id,
                'imagen': curso.URL_PORTADA_CURSO or 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': curso.NOMBRE_CURSO,
                'autor': 'Comunidad ChugChillian',  # si luego agregas autor, se mejora
                'duracion': f"{curso.DURACION_TOTAL_CURSO} horas",
                'descripcion': curso.DESCRIPCION_CURSO,
                'nivel': curso.ESTADO_PUBLICACION_CURSO,
                'precio': str(curso.COSTO_TOTAL_CURSO),
                'puntuacion': float(curso.PUNTUACION_GENERAL_CURSO),
                'items': curso.ITEM_TOTAL_CURSO,
                'suscriptores': curso.SUBSCRIPCION_TOTAL_CURSO
            })

        return JsonResponse({'cursos': cursos}, safe=False)


class CursoDetalleView(View):
    template_name = 'cursos/catalogo/detalle.html'

    def get(self, request, id):
        curso = get_object_or_404(CURSO, id=id)

        requisitos = REQUISITO.objects.filter(curso=curso, ESTADO_REQUISITO=True)
        politicas = POLITICA.objects.filter(curso=curso, ESTADO_POLITICA=True)

        secciones = (
            ACTXCUR.objects
            .filter(curso=curso, ESTADO_ACTXCUR=True)
            .prefetch_related('actividades')
            .order_by('ORDEN_SECCION_CURSO')
        )

        total_secciones = secciones.count()
        total_clases = ACTIVIDAD.objects.filter(seccion__curso=curso).count()

        # 👇 NUEVO: verificar si el usuario ya está inscrito
        ya_inscrito = False
        if request.user.is_authenticated:
            ya_inscrito = CURXUSE.objects.filter(
                usuario=request.user,
                curso=curso,
                ESTADO_CURXUSE=True
            ).exists()

        context = {
            'curso': curso,
            'requisitos': requisitos,
            'politicas': politicas,
            'secciones': secciones,
            'total_secciones': total_secciones,
            'total_clases': total_clases,
            'ya_inscrito': ya_inscrito,  # 👈 lo mandamos al template
        }

        return render(request, self.template_name, context)


class CursoDetalleViewAjax(View):

    def get(self, request, id):
        curso_actual = CURSO.objects.get(id=id)

        # Cursos relacionados (excluimos el actual)
        cursos = CURSO.objects.filter(
            ESTADO_CURSO=True
        ).exclude(id=curso_actual.id)[:4]

        data = []

        for c in cursos:
            data.append({
                "id": c.id,
                "nombre": c.NOMBRE_CURSO,
                "descripcion": c.DESCRIPCION_CURSO[:90] + "...",
                "imagen": c.URL_PORTADA_CURSO or "/static/general/images/inicio/imagen_inicio_portada.png",
                "precio": str(c.COSTO_TOTAL_CURSO),
                "duracion": str(c.DURACION_TOTAL_CURSO),
            })

        return JsonResponse({"cursos": data})


class InscribirCursoView(LoginRequiredMixin, View):

    def get(self, request, id):

        curso = get_object_or_404(CURSO, id=id)

        inscripcion, creada = CURXUSE.objects.get_or_create(
            usuario=request.user,
            curso=curso,
            defaults={'ESTADO_CURXUSE': True}
        )

        if creada:
            messages.success(request, "🎉 ¡Ahora eres parte del aprendizaje!")
        else:
            messages.warning(request, "⚠️ Ya estabas inscrito en este curso.")

        return redirect("mi_aprendizaje")



def obtener_json_actividad_python(id_actividad, usuario=None):
    DEFAULT_AVATAR_URL = "/static/general/images/usuarios/default_avatar.png"  # <- cámbialo si quieres

    actividad = ACTIVIDAD.objects.select_related(
        'tipo_actividad',
        'seccion'
    ).get(id=id_actividad)

    # ======================
    # VIDEO_ACTIVIDAD
    # ======================
    VIDEO_ACTIVIDAD_DATA = list(
        VIDEO_ACTIVIDAD.objects.filter(
            actividad=actividad,
            ESTADO_VIDEO_ACTIVIDAD=True
        ).values(
            'id',
            'actividad_id',
            'URL_VIDEO_ACTIVIDAD',
            'FECHA_INGRESO_VIDEO_ACTIVIDAD',
            'FECHA_MODIFICACION_VIDEO_ACTIVIDAD',
            'ESTADO_VIDEO_ACTIVIDAD'
        )
    )

    # ======================
    # IMAGEN_ACTIVIDAD
    # ======================
    IMAGEN_ACTIVIDAD_DATA = list(
        IMAGEN_ACTIVIDAD.objects.filter(
            actividad=actividad,
            ESTADO_IMAGEN_ACTIVIDAD=True
        ).values(
            'id',
            'actividad_id',
            'URL_IMAGEN_ACTIVIDAD',
            'FECHA_INGRESO_IMAGEN_ACTIVIDAD',
            'FECHA_MODIFICACION_IMAGEN_ACTIVIDAD',
            'ESTADO_IMAGEN_ACTIVIDAD'
        )
    )

    # ======================
    # PDF_ACTIVIDAD
    # ======================
    PDF_ACTIVIDAD_DATA = list(
        PDF_ACTIVIDAD.objects.filter(
            actividad=actividad,
            ESTADO_PDF_ACTIVIDAD=True
        ).values(
            'id',
            'actividad_id',
            'URL_PDF_ACTIVIDAD',
            'FECHA_INGRESO_PDF_ACTIVIDAD',
            'FECHA_MODIFICACION_PDF_ACTIVIDAD',
            'ESTADO_PDF_ACTIVIDAD'
        )
    )

    # ======================
    # DESCRIPCION_ACTIVIDAD
    # ======================
    DESCRIPCION_ACTIVIDAD_DATA = list(
        DESCRIPCION_ACTIVIDAD.objects.filter(
            actividad=actividad,
            ESTADO_DESCRIPCION_ACTIVIDAD=True
        ).values(
            'id',
            'actividad_id',
            'DESCRIPCION_DESCRIPCION_ACTIVIDAD',
            'FECHA_INGRESO_DESCRIPCION_ACTIVIDAD',
            'FECHA_MODIFICACION_DESCRIPCION_ACTIVIDAD',
            'ESTADO_DESCRIPCION_ACTIVIDAD'
        )
    )

    # ======================
    # FORO
    # ======================
    FORO_DATA = FORO.objects.filter(
        actividad=actividad,
        ESTADO_FORO=True
    ).values(
        'id',
        'actividad_id',
        'NOMBRE_FORO',
        'DESCRIPCION_FORO',
        'FECHA_INGRESO_FORO',
        'FECHA_MODIFICACION_FORO',
        'ESTADO_FORO'
    ).first()

    # ======================
    # OPINION_ACTIVIDAD
    # ======================
    OPINION_ACTIVIDAD_DATA = list(
        OPINION_ACTIVIDAD.objects.filter(
            actividad=actividad,
            ESTADO_OPINION_ACTIVIDAD=True
        )
        .select_related('usuario__avatar')  # seguimos la relación hasta AVATAR
        .values(
            'id',
            'usuario_id',
            'usuario__PRIMER_NOMBRE_USUARIO',
            'usuario__PRIMER_APELLIDO_USUARIO',
            'usuario__APODO',

            # CAMPOS DEL AVATAR
            'usuario__avatar__id',
            'usuario__avatar__URL_AVATAR',

            'DESCRIPCION_OPINION_ACTIVIDAD',
            'PUNTUACION_OPINION_ACTIVIDAD',
            'FECHA_INGRESO_OPINION_ACTIVIDAD',
            'FECHA_MODIFICACION_OPINION_ACTIVIDAD',
            'ESTADO_OPINION_ACTIVIDAD'
        )
    )
    for op in OPINION_ACTIVIDAD_DATA:
        if op.get('usuario__avatar__URL_AVATAR') is None:
            op['usuario__avatar__URL_AVATAR'] = DEFAULT_AVATAR_URL

    PROMEDIO_PUNTUACION = OPINION_ACTIVIDAD.objects.filter(
        actividad=actividad,
        ESTADO_OPINION_ACTIVIDAD=True
    ).aggregate(
        AVG_PUNTUACION_OPINION_ACTIVIDAD=Avg('PUNTUACION_OPINION_ACTIVIDAD')
    )['AVG_PUNTUACION_OPINION_ACTIVIDAD'] or 0

    # ======================
    # ACTXUSE
    # ======================
    ACTXUSE_DATA = None
    if usuario:
        ACTXUSE_DATA = ACTXUSE.objects.filter(
            usuario=usuario,
            actividad=actividad
        ).values(
            'id',
            'usuario_id',
            'actividad_id',
            'COMPLETO_ACTXUSE',
            'ESTADO_ACTXUSE',
            'FECHA_INGRESO_ACTXUSE',
            'FECHA_MODIFICACION_ACTXUSE'
        ).first()

    # ======================
    # ACTIVIDAD CENTRAL
    # ======================
    ACTIVIDAD_DATA = {
        "id": actividad.id,
        "tipo_actividad_id": actividad.tipo_actividad_id,
        "seccion_id": actividad.seccion_id,
        "NOMBRE_ACTIVIDAD": actividad.NOMBRE_ACTIVIDAD,
        "DURACION_TOTAL_ACTIVIDAD": float(actividad.DURACION_TOTAL_ACTIVIDAD),
        "FECHA_MODIFICACION_ACTIVIDAD": actividad.FECHA_MODIFICACION_ACTIVIDAD,
        "FECHA_INGRESO_ACTIVIDAD": actividad.FECHA_INGRESO_ACTIVIDAD,
        "ESTADO_ACTIVIDAD": actividad.ESTADO_ACTIVIDAD,
        "PUNTUACION_GENERAL_ACTIVIDAD": actividad.PUNTUACION_GENERAL_ACTIVIDAD
    }

    # ======================
    # TIPO_ACTIVIDAD (TABLA RELACIONADA)
    # ======================
    TIPO_ACTIVIDAD_DATA = {
        "id": actividad.tipo_actividad.id,
        "NOMBRE_TIPO_ACTIVIDAD": actividad.tipo_actividad.NOMBRE_TIPO_ACTIVIDAD,
        "FECHA_MODIFICACION_TIPO_ACTIVIDAD": actividad.tipo_actividad.FECHA_MODIFICACION_TIPO_ACTIVIDAD,
        "FECHA_INGRESO_TIPO_ACTIVIDAD": actividad.tipo_actividad.FECHA_INGRESO_TIPO_ACTIVIDAD,
        "ESTADO_TIPO_ACTIVIDAD": actividad.tipo_actividad.ESTADO_TIPO_ACTIVIDAD,
    }

    # ======================
    # JSON FINAL
    # ======================
    return {
        "ACTIVIDAD": ACTIVIDAD_DATA,
        "TIPO_ACTIVIDAD": TIPO_ACTIVIDAD_DATA,
        "VIDEO_ACTIVIDAD": VIDEO_ACTIVIDAD_DATA,
        "IMAGEN_ACTIVIDAD": IMAGEN_ACTIVIDAD_DATA,
        "PDF_ACTIVIDAD": PDF_ACTIVIDAD_DATA,
        "DESCRIPCION_ACTIVIDAD": DESCRIPCION_ACTIVIDAD_DATA,
        "FORO": FORO_DATA,
        "OPINION_ACTIVIDAD": {
            "DATA": OPINION_ACTIVIDAD_DATA,
            "PROMEDIO_PUNTUACION_OPINION_ACTIVIDAD": round(PROMEDIO_PUNTUACION, 2)
        },
        "ACTXUSE": ACTXUSE_DATA
    }

class CursoAprenderView(LoginRequiredMixin, View):
    template_name = 'cursos/actividad/index.html'

    def get(self, request, id):

        # ======================
        # PANEL GENERAL (CURSO)
        # ======================
        curso = get_object_or_404(CURSO, id=id, ESTADO_CURSO=True)

        inscrito = CURXUSE.objects.filter(
            curso=curso,
            usuario=request.user,
            ESTADO_CURXUSE=True
        ).exists()

        if not inscrito:
            messages.warning(request, "Primero debes inscribirte en este curso.")
            return redirect('curso_detalle', id=id)

        # ======================
        # PANEL DERECHO (ORM)
        # ======================
        secciones = (
            ACTXCUR.objects
            .filter(curso=curso, ESTADO_ACTXCUR=True)
            .prefetch_related('actividades__tipo_actividad')
            .order_by('ORDEN_SECCION_CURSO')
        )

        # ======================
        # PANEL IZQUIERDO (PROCEDURE)
        # ======================
        actividad_id = request.GET.get("actividad")

        if actividad_id:
            actividad = get_object_or_404(ACTIVIDAD, id=actividad_id, seccion__curso=curso)
        else:
            primera = secciones.first()
            actividad = primera.actividades.first() if primera else None


        actividad_json = obtener_json_actividad_python(
            actividad.id,
            request.user
        )
        # ======================
        # MÉTRICAS
        # ======================
        total_actividades = ACTIVIDAD.objects.filter(seccion__curso=curso).count()
        progreso_porcentaje = 0  # luego lo automatizas

        # ======================
        # CONTEXTO FINAL
        # ======================
        context = {
            'curso': curso,
            'secciones': secciones,
            'actividad_actual': actividad,
            'actividad_json': actividad_json,
            'total_actividades': total_actividades,
            'progreso_porcentaje': progreso_porcentaje,
        }

        return render(request, self.template_name, context)





class ActividadJsonTestView(View):
    def get(self, request, id_actividad):

        usuario = request.user  # tu USUARIO real
        json_data = obtener_json_actividad_python(id_actividad, usuario)

        return JsonResponse(json_data, safe=False, json_dumps_params={'indent': 2})