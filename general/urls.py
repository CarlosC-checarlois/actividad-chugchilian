from django.contrib import admin
from django.urls import path
from general import views as views_general

urlpatterns = [
    path('', views_general.InicioView.as_view(), name='inicio'),
    path('cursos/', views_general.CursosView.as_view(), name='cursos'),
    path('login/', views_general.LoginView.as_view(), name='login'),
    path('registro/', views_general.RegistroView.as_view(), name='registro'),
    path('contacto/', views_general.ContactoView.as_view(), name='contacto'),
    path('api/chat/', views_general.chat_api, name='chat_api'),

]
