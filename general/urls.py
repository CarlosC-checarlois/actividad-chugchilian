from django.urls import path
from general import views as views_general
from general.class_views_general.RegistroView import RegistroView
from general.class_views_general.LoginView import LoginView
from general.class_views_general.ContactoView import ContactoView
from general.class_views_general.InicioView import InicioView
from cursos.class_views_cursos.CursosView import CursosView

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    #Funcionalidad generalizada de cursos
    # Funcionalidad generalizada de cursos
    # Funcionalidad generalizada de cursos


    path('cursos/{parametros}', CursosView.as_view(), name='panel_busqueda'),
    path('inicio-sesion/', LoginView.as_view(), name='login'),
    path('logout/', views_general.logout_view, name='logout'),

    path('registro/', RegistroView.as_view(), name='registro'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
    # path('panel_usuario/', views_general.PanelUsuarioView.as_view(), name='panel_usuario'),
    path('educacion-sexual/', views_general.educacion_sexual_view, name='educacion_sexual'),
    path('api/chat/', views_general.chat_api, name='chat_api'),
]
