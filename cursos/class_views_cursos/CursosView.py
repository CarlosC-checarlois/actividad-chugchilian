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
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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


def obtener_actividad_base(id_actividad):
    return ACTIVIDAD.objects.select_related(
        'tipo_actividad',
        'seccion',
        'seccion__curso'
    ).get(id=id_actividad)
def construir_actividad_json(actividad):
    return {
        "id": actividad.id,
        "tipo_actividad_id": actividad.tipo_actividad_id,
        "seccion_id": actividad.seccion_id,
        "curso_id": actividad.seccion.curso_id,
        "NOMBRE_ACTIVIDAD": actividad.NOMBRE_ACTIVIDAD,
        "DURACION_TOTAL_ACTIVIDAD": float(actividad.DURACION_TOTAL_ACTIVIDAD),
        "FECHA_MODIFICACION_ACTIVIDAD": actividad.FECHA_MODIFICACION_ACTIVIDAD,
        "FECHA_INGRESO_ACTIVIDAD": actividad.FECHA_INGRESO_ACTIVIDAD,
        "ESTADO_ACTIVIDAD": actividad.ESTADO_ACTIVIDAD,
        "PUNTUACION_GENERAL_ACTIVIDAD": actividad.PUNTUACION_GENERAL_ACTIVIDAD
    }
def construir_tipo_actividad_json(actividad):
    tipo = actividad.tipo_actividad
    return {
        "id": tipo.id,
        "NOMBRE_TIPO_ACTIVIDAD": tipo.NOMBRE_TIPO_ACTIVIDAD,
        "FECHA_MODIFICACION_TIPO_ACTIVIDAD": tipo.FECHA_MODIFICACION_TIPO_ACTIVIDAD,
        "FECHA_INGRESO_TIPO_ACTIVIDAD": tipo.FECHA_INGRESO_TIPO_ACTIVIDAD,
        "ESTADO_TIPO_ACTIVIDAD": tipo.ESTADO_TIPO_ACTIVIDAD
    }
def obtener_videos(actividad):
    return list(VIDEO_ACTIVIDAD.objects.filter(
        actividad=actividad, ESTADO_VIDEO_ACTIVIDAD=True
    ).values())


def obtener_imagenes(actividad):
    return list(IMAGEN_ACTIVIDAD.objects.filter(
        actividad=actividad, ESTADO_IMAGEN_ACTIVIDAD=True
    ).values())


def obtener_pdfs(actividad):
    return list(PDF_ACTIVIDAD.objects.filter(
        actividad=actividad, ESTADO_PDF_ACTIVIDAD=True
    ).values())


def obtener_descripciones(actividad):
    return list(
        DESCRIPCION_ACTIVIDAD.objects
        .filter(actividad=actividad, ESTADO_DESCRIPCION_ACTIVIDAD=True)
        .order_by("ORDEN_DESCRIPCION")
        .values()
    )



def obtener_foro(actividad):
    return FORO.objects.filter(
        actividad=actividad, ESTADO_FORO=True
    ).values().first()
def obtener_opiniones(actividad, default_avatar):
    data = list(
        OPINION_ACTIVIDAD.objects.filter(
            actividad=actividad,
            ESTADO_OPINION_ACTIVIDAD=True
        ).select_related('usuario__avatar').values(
            'id',
            'usuario_id',
            'usuario__PRIMER_NOMBRE_USUARIO',
            'usuario__PRIMER_APELLIDO_USUARIO',
            'usuario__APODO',
            'usuario__avatar__URL_AVATAR',
            'DESCRIPCION_OPINION_ACTIVIDAD',
            'PUNTUACION_OPINION_ACTIVIDAD',
            'FECHA_INGRESO_OPINION_ACTIVIDAD',
            'FECHA_MODIFICACION_OPINION_ACTIVIDAD'
        )
    )

    for op in data:
        if not op.get('usuario__avatar__URL_AVATAR'):
            op['usuario__avatar__URL_AVATAR'] = default_avatar

    return {
        "DATA": data,
        "PROMEDIO_PUNTUACION_OPINION_ACTIVIDAD": calcular_promedio(actividad)
    }
def calcular_promedio(actividad):
    return round(
        OPINION_ACTIVIDAD.objects.filter(
            actividad=actividad,
            ESTADO_OPINION_ACTIVIDAD=True
        ).aggregate(avg=Avg('PUNTUACION_OPINION_ACTIVIDAD'))['avg'] or 0,
        2
    )
def obtener_actividad_usuario(usuario, actividad):
    if not usuario:
        return []

    curso = actividad.seccion.curso

    return list(
        ACTXUSE.objects.filter(
            usuario=usuario,
            actividad__seccion__curso=curso
        ).select_related('actividad').values(
            'id',
            'actividad_id',
            'actividad__NOMBRE_ACTIVIDAD',
            'COMPLETO_ACTXUSE',
            'ESTADO_ACTXUSE'
        )
    )


def calcular_progreso(usuario, actividad):
    if not usuario:
        return 0

    actxuse = obtener_actividad_usuario(usuario, actividad)

    total = len(actxuse)
    completadas = sum(1 for a in actxuse if a['COMPLETO_ACTXUSE'])

    return round((completadas / total) * 100, 2) if total else 0


def obtener_json_actividad_python(id_actividad, usuario=None):
    DEFAULT_AVATAR_URL = "/static/general/images/usuarios/default_avatar.png"

    actividad = obtener_actividad_base(id_actividad)

    return {
        "ACTIVIDAD": construir_actividad_json(actividad),
        "TIPO_ACTIVIDAD": construir_tipo_actividad_json(actividad),
        "VIDEO_ACTIVIDAD": obtener_videos(actividad),
        "IMAGEN_ACTIVIDAD": obtener_imagenes(actividad),
        "PDF_ACTIVIDAD": obtener_pdfs(actividad),
        "DESCRIPCION_ACTIVIDAD": obtener_descripciones(actividad),
        "FORO": obtener_foro(actividad),
        "OPINION_ACTIVIDAD": obtener_opiniones(actividad, DEFAULT_AVATAR_URL),
        "ACTXUSE": obtener_actividad_usuario(usuario, actividad),
        "PROGRESO_CURSO": calcular_progreso(usuario, actividad),
    }

class CursoAprenderView(LoginRequiredMixin, View):
    template_name = 'cursos/actividad/index.html'

    def get(self, request, id):
        curso = get_object_or_404(CURSO, id=id, ESTADO_CURSO=True)

        inscrito = CURXUSE.objects.filter(
            curso=curso,
            usuario=request.user,
            ESTADO_CURXUSE=True
        ).exists()

        if not inscrito:
            messages.warning(request, "Primero debes inscribirte en este curso.")
            return redirect('curso_detalle', id=id)

        secciones = (
            ACTXCUR.objects
            .filter(curso=curso, ESTADO_ACTXCUR=True)
            .prefetch_related('actividades__tipo_actividad')
            .order_by('ORDEN_SECCION_CURSO')
        )

        actividad_id = request.GET.get("actividad")

        if actividad_id:
            actividad = get_object_or_404(ACTIVIDAD, id=actividad_id, seccion__curso=curso)
        else:
            primera = secciones.first()
            actividad = primera.actividades.first()

        actividad_json = obtener_json_actividad_python(
            actividad.id,
            request.user
        )

        ACTXUSE_MAP = {
            int(item["actividad_id"]): bool(item["COMPLETO_ACTXUSE"])
            for item in actividad_json.get("ACTXUSE", [])
        }

        context = {
            "curso": curso,
            "secciones": secciones,
            "actividad_actual": actividad,

            "ACTIVIDAD": actividad_json.get("ACTIVIDAD"),
            "TIPO_ACTIVIDAD": actividad_json.get("TIPO_ACTIVIDAD"),
            "VIDEO_ACTIVIDAD": actividad_json.get("VIDEO_ACTIVIDAD"),
            "IMAGEN_ACTIVIDAD": actividad_json.get("IMAGEN_ACTIVIDAD"),
            "PDF_ACTIVIDAD": actividad_json.get("PDF_ACTIVIDAD"),
            "DESCRIPCION_ACTIVIDAD": actividad_json.get("DESCRIPCION_ACTIVIDAD"),
            "FORO": actividad_json.get("FORO"),
            "OPINION_ACTIVIDAD": actividad_json.get("OPINION_ACTIVIDAD"),
            "PROGRESO_CURSO": round(actividad_json.get("PROGRESO_CURSO",0),2),

            "ACTXUSE_MAP": ACTXUSE_MAP,
        }

        return render(request, self.template_name, context)

@login_required
@csrf_exempt
def marcar_actividad(request):
    if request.method == "POST":
        actividad_id = request.POST.get("actividad_id")
        completado = request.POST.get("completado") == "true"

        act = ACTIVIDAD.objects.get(id=actividad_id)

        actxuse, _ = ACTXUSE.objects.get_or_create(
            usuario=request.user,
            actividad=act,
            defaults={"ESTADO_ACTXUSE": True}
        )

        actxuse.COMPLETO_ACTXUSE = completado
        actxuse.save()

        return JsonResponse({"ok": True})

class ActividadJsonTestView(View):
    def get(self, request, id_actividad):

        usuario = request.user  # tu USUARIO real
        json_data = obtener_json_actividad_python(id_actividad, usuario)

        return JsonResponse(json_data, safe=False, json_dumps_params={'indent': 2})