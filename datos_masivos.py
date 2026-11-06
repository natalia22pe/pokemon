import os
import django
import requests
from django.core.files.base import ContentFile

# 1. Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemon.settings')
django.setup()

from pokeapp.models import Pokemon, Entrenadores, Gimnasio

def poblar_base_datos():
    print("🚀 Iniciando la carga masiva y conexión con la PokéAPI...\n")

    # ==========================================
    # PASO 1: Descargar y guardar Pokémon de la API
    # ==========================================
    print("--- Descargando Pokémon ---")
    cantidad_pokemon = 10  
    
    for i in range(1, cantidad_pokemon + 1):
        url = f"https://pokeapi.co/api/v2/pokemon/{i}"
        respuesta = requests.get(url)
        
        if respuesta.status_code == 200:
            data = respuesta.json()
            
            nombre = data['name'].capitalize()
            peso = float(data['weight'])
            
            tipos = [t['type']['name'] for t in data['types']]
            naturaleza = ", ".join(tipos)
            
            habilidades_lista = [h['ability']['name'] for h in data['abilities']]
            habilidades = ", ".join(habilidades_lista)[:100]
            
            descripcion = f"Pokémon oficial de tipo {naturaleza} obtenido desde la PokéAPI."[:100]
            
            pokemon_obj, creado = Pokemon.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'peso': peso,
                    'nivel': 50,
                    'habilidades': habilidades,
                    'naturaleza': naturaleza,
                    'descripcion': descripcion
                }
            )
            
            img_url = data['sprites']['other']['official-artwork']['front_default']
            if img_url and (creado or not pokemon_obj.imagen):
                img_respuesta = requests.get(img_url)
                if img_respuesta.status_code == 200:
                    nombre_archivo = f"{data['name']}.png"
                    pokemon_obj.imagen.save(nombre_archivo, ContentFile(img_respuesta.content), save=True)
            
            if creado:
                print(f"  [+] Pokémon agregado: {nombre}")
            else:
                print(f"  [=] Pokémon ya existente: {nombre}")
        else:
            print(f"  [X] Error al consultar el Pokémon ID {i}")

    # ==========================================
    # PASO 2: Crear Entrenadores y asignar Pokémon
    # ==========================================
    print("\n--- Registrando Entrenadores ---")
    lista_entrenadores = [
        {"id_documento": 101, "nombre": "Ash", "apellido": "Ketchum", "nombres_pokemones": ["Bulbasaur", "Pikachu"], "medallas": 8},
        {"id_documento": 102, "nombre": "Misty", "apellido": "Waterflower", "nombres_pokemones": ["Squirtle", "Staryu"], "medallas": 5},
        {"id_documento": 103, "nombre": "Brock", "apellido": "Harrison", "nombres_pokemones": ["Onix"], "medallas": 6},
    ]

    for e in lista_entrenadores:
        trainer, creado = Entrenadores.objects.get_or_create(
            id_documento=e["id_documento"],
            defaults={
                "nombre": e["nombre"],
                "apellido": e["apellido"],
                "medallas": e["medallas"],
            }
        )

        if not creado:
            trainer.nombre = e["nombre"]
            trainer.apellido = e["apellido"]
            trainer.medallas = e["medallas"]
            trainer.save()

        # Asignación correcta con .set()
        pokemones_objs = Pokemon.objects.filter(nombre__in=e["nombres_pokemones"])
        trainer.pokemones.set(pokemones_objs)

        estado = "Agregado" if creado else "Actualizado"
        print(f"  [+] Entrenador {estado}: {trainer.nombre} {trainer.apellido}")

    # ==========================================
    # PASO 3: Crear Gimnasios y asignar líderes
    # ==========================================
    print("\n--- Registrando Gimnasios ---")
    
    ash = Entrenadores.objects.filter(nombre="Ash").first()
    misty = Entrenadores.objects.filter(nombre="Misty").first()
    brock = Entrenadores.objects.filter(nombre="Brock").first()

    lista_gimnasios = [
        {"lider": brock, "naturaleza_gym": "Roca", "medallas_gym": "Medalla Roca"},
        {"lider": misty, "naturaleza_gym": "Agua", "medallas_gym": "Medalla Cascada"},
        {"lider": ash, "naturaleza_gym": "Eléctrico", "medallas_gym": "Medalla Trueno"},
    ]

    for g in lista_gimnasios:
        gym, creado = Gimnasio.objects.get_or_create(
            naturaleza_gym=g["naturaleza_gym"],
            defaults={
                "lider": g["lider"],
                "medallas_gym": g["medallas_gym"]
            }
        )
        if not creado:
            gym.lider = g["lider"]
            gym.medallas_gym = g["medallas_gym"]
            gym.save()
            print(f"  [=] Gimnasio actualizado de tipo: {gym.naturaleza_gym}")
        else:
            print(f"  [+] Gimnasio creado de tipo: {gym.naturaleza_gym}")

    print("\n¡Proceso de carga masiva finalizado con éxito! 🎉")

# ESTO ES LO QUE EJECUTA LA FUNCIÓN AL CORRER EL SCRIPT
if __name__ == '__main__':
    poblar_base_datos()