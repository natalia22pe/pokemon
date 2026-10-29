
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
    path('agregar/', views.crear_pokemon, name='agregar_pokemon'),
    path('editar/<int:pk>/', views.editar_pokemon, name='editar_pokemon'),
    path('eliminar/<int:pk>/', views.eliminar_pokemon, name='eliminar_pokemon'),
    
    # Rutas de Autenticación
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)