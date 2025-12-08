from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse

class LoginView(View):
    template_name = 'general/login/index.html'

    def get(self, request):
        return render(request, self.template_name, {
            'titulo_pagina': 'Iniciar Sesión — Comunidad ChugChillian'
        })

    def post(self, request):

        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.GET.get('next')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            messages.success(request, "🌱 Bienvenido a ChugChillian")

            # redirigir a donde iba o al inicio
            if next_url:
                return redirect(next_url)
            return redirect('inicio')

        else:
            messages.error(request, "❌ Correo o contraseña incorrectos")
            return redirect('login')
