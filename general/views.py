from django.views.generic import TemplateView
import os
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class InicioView(TemplateView):
    template_name = 'general/inicio/index.html'
    extra_context = {
        'titulo_pagina': 'ChugChillian — Educación y Cultura Viva',
    }


class CursosView(TemplateView):
    template_name = 'general/cursos/index.html'
    extra_context = {
        'titulo_pagina': 'ChugChillian — Cursos Comunitarios',

        'cursos': [
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '🌾 Agricultura Sostenible',
                'autor': 'Comunidad ChugChillian',
                'duracion': '6 horas',
                'descripcion': 'Aprende técnicas ancestrales de cultivo combinadas con prácticas modernas para preservar la tierra y mejorar la productividad.',
                'nivel': 'Básico',
                'nivel_color': 'success',
                'precio': '15.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '🗣️ Lengua Kichwa',
                'autor': 'Maestra Nina',
                'duracion': '8 horas',
                'descripcion': 'Descubre la riqueza del idioma Kichwa: su gramática, su conexión con la naturaleza y su valor en la identidad de los pueblos andinos.',
                'nivel': 'Intermedio',
                'nivel_color': 'primary',
                'precio': '18.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '🎨 Artes y Tradiciones',
                'autor': 'Taller Cultural Ñawi',
                'duracion': '5 horas',
                'descripcion': 'Aprende sobre música, danza, tejidos y pintura tradicional. Cada clase revive la memoria cultural de nuestra comunidad.',
                'nivel': 'Avanzado',
                'nivel_color': 'info',
                'precio': '22.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '🌱 Reforestación y Cuidado Ambiental',
                'autor': 'EcoSaberes Comunitarios',
                'duracion': '7 horas',
                'descripcion': 'Participa en proyectos de reforestación y conoce las especies nativas que ayudan a mantener el equilibrio ecológico de nuestra región.',
                'nivel': 'Básico',
                'nivel_color': 'success',
                'precio': '12.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '🧵 Tejidos Ancestrales',
                'autor': 'Artesanas Ñusta',
                'duracion': '9 horas',
                'descripcion': 'Descubre las técnicas de tejido tradicional que reflejan la cosmovisión andina y preservan la memoria de nuestros pueblos.',
                'nivel': 'Avanzado',
                'nivel_color': 'warning',
                'precio': '25.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '📸 Fotografía Cultural',
                'autor': 'Escuela Visual Runa',
                'duracion': '10 horas',
                'descripcion': 'Aprende a capturar la esencia de la vida comunitaria, la naturaleza y las tradiciones a través de la fotografía documental.',
                'nivel': 'Intermedio',
                'nivel_color': 'primary',
                'precio': '20.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '💞 Educación Sexual Integral',
                'autor': 'Equipo de Salud Comunitaria Ñawi',
                'duracion': '10 horas',
                'descripcion': 'Aprende sobre el respeto, la igualdad y la salud sexual desde una perspectiva integral y culturalmente sensible. Este curso promueve el diálogo, la prevención y el bienestar comunitario.',
                'nivel': 'Intermedio',
                'nivel_color': 'danger',
                'precio': '18.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '🎭 Teatro Comunitario',
                'autor': 'Colectivo Ñawi Pacha',
                'duracion': '6 horas',
                'descripcion': 'Explora el teatro como una herramienta de expresión colectiva, sanación y fortalecimiento de la identidad cultural.',
                'nivel': 'Básico',
                'nivel_color': 'success',
                'precio': '16.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '🥁 Música y Sonidos del Pueblo',
                'autor': 'Escuela Kawsay',
                'duracion': '8 horas',
                'descripcion': 'Sumérgete en los ritmos tradicionales andinos y aprende a crear instrumentos musicales con materiales naturales.',
                'nivel': 'Avanzado',
                'nivel_color': 'info',
                'precio': '24.00',
            },
            {
                'imagen': 'general/images/inicio/imagen_inicio_portada.png',
                'titulo': '📖 Escritura y Relato Oral',
                'autor': 'Maestros de la Palabra',
                'duracion': '5 horas',
                'descripcion': 'Desarrolla tus habilidades narrativas y aprende a transmitir la memoria colectiva mediante la escritura y la oralidad.',
                'nivel': 'Intermedio',
                'nivel_color': 'primary',
                'precio': '19.00',
            },
        ]
    }


class LoginView(TemplateView):
    template_name = 'general/login/index.html'
    extra_context = {
        'titulo_pagina': 'Iniciar Sesión — Comunidad ChugChillian',
    }


class RegistroView(TemplateView):
    template_name = 'general/register/index.html'
    extra_context = {
        'titulo_pagina': 'Crear Cuenta — Comunidad ChugChillian',
    }


class ContactoView(TemplateView):
    template_name = 'general/contacto/index.html'
    extra_context = {
        'titulo_pagina': 'Contacto — Comunidad ChugChillian',
    }

import os
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "ac8819c2-ee7a-4b81-8080-fa245705b1f2"))

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")

            if not message:
                return JsonResponse({"reply": "Por favor, escribe un mensaje."})

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente útil y amable."},
                    {"role": "user", "content": message},
                ]
            )

            reply = completion.choices[0].message.content.strip()
            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": f"Error: {str(e)}"})

    return JsonResponse({"reply": "Método no permitido."}, status=405)
