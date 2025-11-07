from django.urls import path

from . import views

urlpatterns = [
    path('adopciones/', views.lista_adopciones, name='listaAdopcion'),
    path('adopciones/nueva/', views.nueva_adopcion, name='nuevaAdopcion'),
    path('adopciones/guardar/', views.guardar_adopcion, name='guardarAdopcion'),
    path('adopciones/editar/<int:pk>/', views.editar_adopcion, name='editarAdopcion'),
    path('adopciones/actualizar/<int:pk>/', views.actualizar_adopcion, name='actualizarAdopcion'),
    path('adopciones/eliminar/<int:pk>/', views.eliminar_adopcion, name='eliminarAdopcion'),
    path('', views.analisis_adopciones, name='analisisAdopcion'),
]