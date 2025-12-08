from django.views.generic import TemplateView
import os
import openai

from django.shortcuts import render, redirect
from django.views import View
import os
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.shortcuts import redirect

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


class PanelUsuarioView(View):
    template_name = 'general/panel/usuario/index.html'

    def get(self, request):
        usuario = request.session.get('usuario')
        return render(request, self.template_name, {'usuario': usuario})




def logout_view(request):
    logout(request)
    return redirect('inicio')

def educacion_sexual_view(request):
    return render(request, 'general/educacion_sexual/index.html')
