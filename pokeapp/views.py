import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import Pokemon, Entrenadores, Gimnasio
from .forms import PokemonForm, EntrenadorForm, GimnasioForm


# ==========================================
# VISTAS PRINCIPALES Y APIS EXTERNAS
# ==========================================

def index(request):
    # 1. Búsqueda en la Base de Datos Local
    query = request.GET.get('q', '')
    if query:
        pokemons = Pokemon.objects.filter(nombre__icontains=query)
    else:
        pokemons = Pokemon.objects.all()

    # 2. Búsqueda en la PokéAPI (Datos de Pokémon)
    pokemon_api = None
    error_api = None
    nombre_api = request.GET.get('nombre', '').strip().lower()

    if nombre_api:
        try:
            url_pokeapi = f"https://pokeapi.co/api/v2/pokemon/{nombre_api}"
            res_poke = requests.get(url_pokeapi, timeout=5)
            if res_poke.status_code == 200:
                pokemon_api = res_poke.json()
            else:
                error_api = f"No se encontró el Pokémon '{nombre_api}' en la PokéAPI."
        except Exception:
            error_api = "Error al conectar con la PokéAPI."

    # 3. Búsqueda en Pokémon TCG API (Cartas Coleccionables)
    carta_tcg = None
    error_tcg = None
    nombre_carta = request.GET.get('carta', '').strip()

    if nombre_carta:
        try:
            url_tcg = f"https://api.pokemontcg.io/v2/cards?q=name:{nombre_carta}"
            res_tcg = requests.get(url_tcg, timeout=5)
            if res_tcg.status_code == 200:
                datos_tcg = res_tcg.json()
                if datos_tcg.get('data'):
                    # Retorna los datos de la primera carta encontrada
                    carta_tcg = datos_tcg['data'][0]
                else:
                    error_tcg = f"No se encontraron cartas para '{nombre_carta}'."
            else:
                error_tcg = "No se pudo consultar la API de Cartas TCG."
        except Exception:
            error_tcg = "Error de conexión con Pokémon TCG API."

    # Renderizamos la plantilla index.html con todos los contextos unidos
    return render(request, 'pokeapp/index.html', {
        'pokemons': pokemons,
        'query': query,
        'pokemon': pokemon_api,
        'error': error_api,
        'nombre_api': nombre_api,
        'carta_tcg': carta_tcg,
        'error_tcg': error_tcg,
        'nombre_carta': nombre_carta,
    })


def buscar_pokemon(request):
    """
    Vista individual opcional para buscar en la PokéAPI si tienes una ruta separada.
    """
    pokemon_data = None
    error = None

    if 'nombre' in request.GET:
        nombre = request.GET.get('nombre').strip().lower()
        if nombre:
            try:
                url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
                respuesta = requests.get(url, timeout=5)
                if respuesta.status_code == 200:
                    pokemon_data = respuesta.json()
                else:
                    error = "No se encontró ningún Pokémon con ese nombre."
            except Exception:
                error = "Error al conectar con el servidor de la API."

    return render(request, 'pokeapp/index.html', {
        'pokemon': pokemon_data,
        'error': error
    })


# ==========================================
# AUTENTICACIÓN
# ==========================================

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'pokeapp/login.html', {'form': form})


# ==========================================
# VISTAS DE POKÉMON (CRUD LOCAL)
# ==========================================

def detalle_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    return render(request, 'pokeapp/detalle.html', {'pokemon': pokemon})


@login_required(login_url='/accounts/login/')
def crear_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PokemonForm()
    return render(request, 'pokeapp/crear_pokemon.html', {'form': form})


@login_required(login_url='/accounts/login/')
def editar_pokemon(request, pk):
    pokemon = get_object_or_404(Pokemon, pk=pk)
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('detalle_pokemon', pokemon_id=pokemon.id)
    else:
        form = PokemonForm(instance=pokemon)
    return render(request, 'pokeapp/editar_pokemon.html', {'form': form, 'pokemon': pokemon})


@login_required(login_url='/accounts/login/')
def eliminar_pokemon(request, pk):
    pokemon = get_object_or_404(Pokemon, pk=pk)
    if request.method == 'POST':
        pokemon.delete()
        return redirect('index')
    return render(request, 'pokeapp/eliminar_pokemon.html', {'pokemon': pokemon})


# ==========================================
# VISTAS DE ENTRENADORES (CRUD LOCAL)
# ==========================================

def lista_entrenadores(request):
    entrenadores = Entrenadores.objects.all()
    return render(request, 'pokeapp/entrenadores.html', {'entrenadores': entrenadores})


@login_required(login_url='/accounts/login/')
def crear_entrenador(request):
    if request.method == 'POST':
        form = EntrenadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entrenadores')
    else:
        form = EntrenadorForm()
    return render(request, 'pokeapp/crear_entrenador.html', {'form': form})


@login_required(login_url='/accounts/login/')
def editar_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenadores, pk=pk)
    if request.method == 'POST':
        form = EntrenadorForm(request.POST, instance=entrenador)
        if form.is_valid():
            form.save()
            return redirect('entrenadores')
    else:
        form = EntrenadorForm(instance=entrenador)
    return render(request, 'pokeapp/editar_entrenador.html', {'form': form, 'entrenador': entrenador})


@login_required(login_url='/accounts/login/')
def eliminar_entrenador(request, pk):
    entrenador = get_object_or_404(Entrenadores, pk=pk)
    if request.method == 'POST':
        entrenador.delete()
        return redirect('entrenadores')
    return render(request, 'pokeapp/eliminar_entrenador.html', {'entrenador': entrenador})


# ==========================================
# VISTAS DE GIMNASIOS (CRUD LOCAL)
# ==========================================

def lista_gimnasios(request):
    gimnasios = Gimnasio.objects.all()
    return render(request, 'pokeapp/Gimnasio.html', {'gimnasios': gimnasios})


@login_required(login_url='/accounts/login/')
def crear_gimnasio(request):
    if request.method == 'POST':
        form = GimnasioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gimnasios')
    else:
        form = GimnasioForm()
    return render(request, 'pokeapp/crear_gimnasio.html', {'form': form})


@login_required(login_url='/accounts/login/')
def editar_gimnasio(request, pk):
    gimnasio = get_object_or_404(Gimnasio, pk=pk)
    if request.method == 'POST':
        form = GimnasioForm(request.POST, instance=gimnasio)
        if form.is_valid():
            form.save()
            return redirect('gimnasios')
    else:
        form = GimnasioForm(instance=gimnasio)
    return render(request, 'pokeapp/editar_gimnasio.html', {'form': form, 'gimnasio': gimnasio})


@login_required(login_url='/accounts/login/')
def eliminar_gimnasio(request, pk):
    gimnasio = get_object_or_404(Gimnasio, pk=pk)
    if request.method == 'POST':
        gimnasio.delete()
        return redirect('gimnasios')
    return render(request, 'pokeapp/eliminar_gimnasio.html', {'gimnasio': gimnasio})

import random

def adivina_pokemon(request):
    pokemon_misterioso = None
    resultado = None
    
    # Si el usuario envió su intento por el formulario
    if request.method == 'POST':
        intentos = request.POST.get('intento', '').strip().lower()
        nombre_real = request.POST.get('nombre_real', '').lower()
        
        if intentos == nombre_real:
            resultado = f" ¡Correcto! Era {nombre_real.capitalize()}."
        else:
            resultado = f" Incorrecto. Era {nombre_real.capitalize()}."
            
        # Generamos uno nuevo para seguir jugando
        id_aleatorio = random.randint(1, 151)
    else:
        # Primer cargue del juego: ID aleatorio
        id_aleatorio = random.randint(1, 151)

    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{id_aleatorio}"
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            pokemon_misterioso = respuesta.json()
    except Exception:
        pass

    return render(request, 'pokeapp/adivina.html', {
        'pokemon': pokemon_misterioso,
        'resultado': resultado
    })