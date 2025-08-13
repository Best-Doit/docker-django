from django.urls import path
from . import views

app_name = 'docs_pdf'


urlpatterns = [
    path('', views.convertir_documento, name='convertir_documento'),
    path('descargar/<str:filename>/', views.descargar_archivo, name='descargar_archivo'),
]
