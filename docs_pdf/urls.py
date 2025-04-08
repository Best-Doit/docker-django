from django.urls import path
from . import views

app_name = 'docs_pdf'


urlpatterns = [
    path('', views.convertir_word_pdf, name='convertir_word_pdf'),
    path('descargar-pdf/<str:filename>/', views.descargar_pdf, name='descargar_pdf'),
]
