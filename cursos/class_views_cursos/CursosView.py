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
            'ya_inscrito': ya_inscrito,   # 👈 lo mandamos al template
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



class CursoAprenderView(LoginRequiredMixin, View):
    """
    Vista tipo 'player' donde el estudiante ve el contenido del curso.
    Requiere estar autenticado e inscrito en el curso.
    """
    template_name = 'cursos/actividad/index.html'

    def get(self, request, id):
        # 1. Obtener curso
        curso = get_object_or_404(CURSO, id=id, ESTADO_CURSO=True)

        # 2. Verificar que el usuario esté inscrito
        inscrito = CURXUSE.objects.filter(
            curso=curso,
            usuario=request.user,
            ESTADO_CURXUSE=True
        ).exists()

        if not inscrito:
            messages.warning(request, "Primero debes inscribirte en este curso.")
            return redirect('curso_detalle', id=id)

        # 3. Traer secciones + actividades
        secciones = (
            ACTXCUR.objects
            .filter(curso=curso, ESTADO_ACTXCUR=True)
            .prefetch_related('actividades')
            .order_by('ORDEN_SECCION_CURSO')
        )

        # 4. Actividad actual (por ?actividad=ID) o la primera actividad del curso
        actividad_id = request.GET.get("actividad")
        actividad_actual = None

        if actividad_id:
            actividad_actual = get_object_or_404(
                ACTIVIDAD,
                id=actividad_id,
                seccion__curso=curso
            )
        else:
            primera_seccion = secciones.first()
            if primera_seccion:
                # Ajusta el orden según tu modelo de ACTIVIDAD
                actividad_actual = primera_seccion.actividades.first()

        # 5. (Opcional) cálculos de progreso
        total_actividades = ACTIVIDAD.objects.filter(seccion__curso=curso).count()
        progreso_porcentaje = 0  # luego puedes calcularlo de verdad

        context = {
            'curso': curso,
            'secciones': secciones,
            'actividad_actual': actividad_actual,
            'total_actividades': total_actividades,
            'progreso_porcentaje': progreso_porcentaje,
        }
        return render(request, self.template_name, context)