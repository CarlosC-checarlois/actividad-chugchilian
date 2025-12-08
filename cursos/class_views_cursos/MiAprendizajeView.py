from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView
from cursos.models import CURSO
from cursos.models import CURXUSE

class MiAprendizajeView(LoginRequiredMixin, TemplateView):
    template_name = "cursos/usuario/mi_aprendizaje/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cursos = CURXUSE.objects.filter(usuario=self.request.user)
        context["mis_cursos"] = cursos
        return context