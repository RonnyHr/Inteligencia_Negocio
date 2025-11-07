from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_mascotas, name='listaMascota'),
    path('nueva/', views.nueva_mascota, name='nuevaMascota'),
    path('guardar/', views.guardar_mascota, name='guardarMascota'),
    path('editar/<int:pk>/', views.editar_mascota, name='editarMascota'),
    path('actualizar/<int:pk>/', views.actualizar_mascota, name='actualizarMascota'),
    path('eliminar/<int:pk>/', views.eliminar_mascota, name='eliminarMascota'),
]
