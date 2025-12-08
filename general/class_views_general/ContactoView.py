from django.views.generic import TemplateView
import os
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages



import os
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
class ContactoView(TemplateView):
    template_name = 'general/contacto/index.html'
    extra_context = {
        'titulo_pagina': 'Contacto — Comunidad ChugChillian',
    }