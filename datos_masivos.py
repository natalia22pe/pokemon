import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemon.settings')
django.setup()

from pokeapp.models import Pokemon, Gimnasio, Entrenadores

def poblar_base_datos():
    print("Iniciando la carga masiva de datos...")

    # 1. Crear Entrenadores (con sus campos correspondientes)
    lista_entrenadores = [
        {"id_documento": 101, "nombre": "Ash", "apellido": "Ketchum", "pokemones": "Pikachu", "medallas": 8},
        {"id_documento": 102, "nombre": "Misty", "apellido": "Waterflower", "pokemones": "Staryu", "medallas": 5},
        {"id_documento": 103, "nombre": "Brock", "apellido": "Harrison", "pokemones": "Onix", "medallas": 6},
        {"id_documento": 104, "nombre": "Gary", "apellido": "Oak", "pokemones": "Eevee", "medallas": 9},
        {"id_documento": 105, "nombre": "Jessie", "apellido": "Rocket", "pokemones": "Wobbuffet", "medallas": 0},
        {"id_documento": 106, "nombre": "James", "apellido": "Rocket", "pokemones": "Koffing", "medallas": 0},
        {"id_documento": 107, "nombre": "Blaine", "apellido": "Fuego", "pokemones": "Magmar", "medallas": 7},
        {"id_documento": 108, "nombre": "Sabrina", "apellido": "Psíquica", "pokemones": "Alakazam", "medallas": 7},
        {"id_documento": 109, "nombre": "Lt.", "apellido": "Surge", "pokemones": "Raichu", "medallas": 4},
        {"id_documento": 110, "nombre": "Erika", "apellido": "Planta", "pokemones": "Vileplume", "medallas": 5},
    ]

    for e in lista_entrenadores:
        trainer, creado = Entrenadores.objects.get_or_create(
            id_documento=e["id_documento"],
            defaults={
                "nombre": e["nombre"],
                "apellido": e["apellido"],
                "pokemones": e["pokemones"],
                "medallas": e["medallas"]
            }
        )
        if creado:
            print(f"-> Entrenador agregado: {trainer.nombre}")

    # 2. Crear Gimnasios (usando lider_del_GYM, Naturaleza_de_GYM, Medallas)
    gimnasios = [
        {"lider": "Brock", "naturaleza": "Roca", "medalla": "Medalla Roca"},
        {"lider": "Misty", "naturaleza": "Agua", "medalla": "Medalla Cascada"},
        {"lider": "Lt. Surge", "naturaleza": "Eléctrico", "medalla": "Medalla Trueno"},
        {"lider": "Erika", "naturaleza": "Planta", "medalla": "Medalla Arcoíris"},
        {"lider": "Koga", "naturaleza": "Veneno", "medalla": "Medalla Alma"},
        {"lider": "Sabrina", "naturaleza": "Psíquico", "medalla": "Medalla Pantano"},
        {"lider": "Blaine", "naturaleza": "Fuego", "medalla": "Medalla Volcán"},
        {"lider": "Giovanni", "naturaleza": "Tierra", "medalla": "Medalla Tierra"},
    ]
    
    for g in gimnasios:
        gym, creado = Gimnasio.objects.get_or_create(
            lider_del_GYM=g["lider"],
            defaults={
                "Naturaleza_de_GYM": g["naturaleza"],
                "Medallas": g["medalla"]
            }
        )
        if creado:
            print(f"-> Gimnasio agregado: {gym.lider_del_GYM}")

    # 3. Crear los 15 Pokémon (con sus atributos completos)
    lista_pokemones = [
        {"nombre": "Bulbasaur", "peso": 6.9, "habilidades": "Espesura", "naturaleza": "Mansos", "descripcion": "Planta/Veneno"},
        {"nombre": "Ivysaur", "peso": 13.0, "habilidades": "Espesura", "naturaleza": "Docil", "descripcion": "Evolución de Bulbasaur"},
        {"nombre": "Venusaur", "peso": 100.0, "habilidades": "Espesura", "naturaleza": "Fuerte", "descripcion": "Planta grande"},
        {"nombre": "Charmander", "peso": 8.5, "habilidades": "Mar Llamas", "naturaleza": "Alegre", "descripcion": "Fuego puro"},
        {"nombre": "Charmeleon", "peso": 19.0, "habilidades": "Mar Llamas", "naturaleza": "Activo", "descripcion": "Cola de fuego"},
        {"nombre": "Charizard", "peso": 90.5, "habilidades": "Mar Llamas", "naturaleza": "Firme", "descripcion": "Dragón de fuego"},
        {"nombre": "Squirtle", "peso": 9.0, "habilidades": "Torrente", "naturaleza": "Sereno", "descripcion": "Tortuga de agua"},
        {"nombre": "Wartortle", "peso": 22.5, "habilidades": "Torrente", "naturaleza": "Calmado", "descripcion": "Orejas peludas"},
        {"nombre": "Blastoise", "peso": 85.5, "habilidades": "Torrente", "naturaleza": "Robusto", "descripcion": "Cañones de agua"},
        {"nombre": "Caterpie", "peso": 2.9, "habilidades": "Polvo Escudo", "naturaleza": "Timido", "descripcion": "Bicho verde"},
        {"nombre": "Metapod", "peso": 9.9, "habilidades": "Mudar", "naturaleza": "Plácido", "descripcion": "Capullo duro"},
        {"nombre": "Butterfree", "peso": 32.0, "habilidades": "Ojo Compuesto", "naturaleza": "Amable", "descripcion": "Mariposa"},
        {"nombre": "Weedle", "peso": 3.2, "habilidades": "Polvo Escudo", "naturaleza": "Huraño", "descripcion": "Bicho ponzoñoso"},
        {"nombre": "Kakuna", "peso": 10.0, "habilidades": "Mudar", "naturaleza": "Dócil", "descripcion": "Capullo inmóvil"},
        {"nombre": "Beedrill", "peso": 29.5, "habilidades": "Enjambre", "naturaleza": "Agresivo", "descripcion": "Abeja asesina"},
    ]

    for p in lista_pokemones:
        poke, creado = Pokemon.objects.get_or_create(
            nombre=p["nombre"],
            defaults={
                "peso": p["peso"],
                "habilidades": p["habilidades"],
                "naturaleza": p["naturaleza"],
                "descripcion": p["descripcion"]
            }
        )
        if creado:
            print(f"-> Pokémon agregado: {poke.nombre}")

    print("¡Carga masiva completada con éxito en PostgreSQL!")

if __name__ == '__main__':
    poblar_base_datos()