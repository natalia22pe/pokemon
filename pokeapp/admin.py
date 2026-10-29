


from django.contrib import admin
from .models import Entrenadores, Gimnasio, Pokemon

@admin.register(Entrenadores)
class EntrenadoresAdmin(admin.ModelAdmin):
    list_display = ('id_documento', 'nombre', 'apellido', 'pokemones', 'medallas')
    search_fields = ('nombre', 'apellido', 'id_documento')

@admin.register(Gimnasio)
class GimnasioAdmin(admin.ModelAdmin):
    list_display = ('lider_del_GYM', 'Naturaleza_de_GYM', 'Medallas')
    search_fields = ('lider_del_GYM', 'Naturaleza_de_GYM')

@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'peso', 'naturaleza', 'habilidades', 'entrenador')
    search_fields = ('nombre', 'naturaleza', 'habilidades')
    list_filter = ('naturaleza', 'habilidades')