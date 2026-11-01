from django.contrib import admin
from .models import Entrenadores, Gimnasio, Pokemon

@admin.register(Entrenadores)
class EntrenadoresAdmin(admin.ModelAdmin):
    list_display = ('id_documento', 'nombre', 'apellido', 'medallas')
    search_fields = ('nombre', 'apellido', 'id_documento')

@admin.register(Gimnasio)
class GimnasioAdmin(admin.ModelAdmin):
    list_display = ('id', 'lider', 'naturaleza_gym', 'medallas_gym')
    search_fields = ('naturaleza_gym',)

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'nivel', 'peso', 'naturaleza')
    search_fields = ('nombre', 'naturaleza')