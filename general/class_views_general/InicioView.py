from django.views.generic import TemplateView
import os
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

class InicioView(TemplateView):
    template_name = 'general/inicio/index.html'
    extra_context = {
        'titulo_pagina': 'ChugChillian — Educación y Cultura Viva',
    }
