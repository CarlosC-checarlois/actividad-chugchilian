from django.urls import path
from cursos.class_views_cursos.MiAprendizajeView import MiAprendizajeView
from cursos.class_views_cursos.CursosView import CursosView, CursosViewAjax, CursoDetalleView, CursoDetalleViewAjax, \
    InscribirCursoView, CursoAprenderView, ActividadJsonTestView

# La url empieza con CURSOS/
urlpatterns = [
    path('mi-aprendizaje/', MiAprendizajeView.as_view(), name='mi_aprendizaje'),
    path('', CursosView.as_view(), name='cursos'),
    path('ajax/', CursosViewAjax.as_view(), name='cursos_ajax'),
    path('detalle/<int:id>/', CursoDetalleView.as_view(), name='curso_detalle'),
    path('detalle/ajax/<int:id>/', CursoDetalleViewAjax.as_view(), name='curso_detalle_ajax'),
    path('inscripcion/<int:id>/', InscribirCursoView.as_view(), name='inscribirse_curso'),
    path('aprender/<int:id>/', CursoAprenderView.as_view(), name='curso_aprender'),
    path('test-actividad/<int:id_actividad>/', ActividadJsonTestView.as_view(), name='test_actividad'),

]