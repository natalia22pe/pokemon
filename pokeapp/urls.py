
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from pokeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('pokemon/<int:pokemon_id>/', views.detalle_pokemon, name='detalle_pokemon'),
    path('agregar/', views.crear_pokemon, name='crear_pokemon'),
    path('editar/<int:pk>/', views.editar_pokemon, name='editar_pokemon'),
    path('eliminar/<int:pk>/', views.eliminar_pokemon, name='eliminar_pokemon'),
    
    # Rutas para Entrenadores
    path('entrenadores/', views.lista_entrenadores, name='entrenadores'),
    path('entrenadores/nuevo/', views.crear_entrenador, name='crear_entrenador'), # <-- ¡Asegúrate de tener esta línea!
    path('entrenadores/editar/<int:pk>/', views.editar_entrenador, name='editar_entrenador'),
    path('entrenadores/eliminar/<int:pk>/', views.eliminar_entrenador, name='eliminar_entrenador'),
    # Rutas para Gimnasios
    
    # Rutas para Gimnasios
    path('gimnasios/', views.lista_gimnasios, name='gimnasios'),
    path('gimnasios/nuevo/', views.crear_gimnasio, name='crear_gimnasio'),  # <-- ¡Agrega esta línea aquí!
    path('gimnasios/editar/<int:pk>/', views.editar_gimnasio, name='editar_gimnasio'),
    path('gimnasios/eliminar/<int:pk>/', views.eliminar_gimnasio, name='eliminar_gimnasio'),
    
    # Rutas de Autenticación
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)