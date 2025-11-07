from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_persona, name='listaPersona'),
    path('nueva/', views.nueva_persona, name='nuevaPersona'),
    path('guardar/', views.guardar_persona, name='guardarPersona'),
    path('editar/<int:pk>/', views.editar_persona, name='editarPersona'),
    path('actualizar/<int:pk>/', views.actualizar_persona, name='actualizarPersona'),
    path('eliminar/<int:pk>/', views.eliminar_persona, name='eliminarPersona'),
]
