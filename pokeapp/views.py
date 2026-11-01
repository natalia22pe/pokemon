from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Pokemon, Entrenadores, Gimnasio
from .forms import PokemonForm, EntrenadorForm, GimnasioForm

# ==========================================
# VISTAS DE POKÉMON
# ==========================================

def index(request):
    query = request.GET.get('q', '')
    if query:
        pokemons = Pokemon.objects.filter(nombre__icontains=query)
    else:
        pokemons = Pokemon.objects.all()
        
    return render(request, 'pokeapp/index.html', {'pokemons': pokemons, 'query': query})

def detalle_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    return render(request, 'pokeapp/detalle.html', {'pokemon': pokemon})

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
# VISTAS DE ENTRENADORES
# ==========================================

def lista_entrenadores(request):
    entrenadores = Entrenadores.objects.all()
    return render(request, 'pokeapp/entrenadores.html', {'entrenadores': entrenadores})

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
# VISTAS DE GIMNASIOS
# ==========================================

def lista_gimnasios(request):
    gimnasios = Gimnasio.objects.all()
    return render(request, 'pokeapp/Gimnasio.html', {'gimnasios': gimnasios})

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
from django.shortcuts import render, redirect, get_object_or_404
from .models import Gimnasio
# Asegúrate de tener importado tu formulario de gimnasio (o créalo si falta)

def crear_gimnasio(request):
    if request.method == 'POST':
        # Aquí procesas los datos del formulario para guardarlos
        lider = request.POST.get('lider')
        naturaleza_gym = request.POST.get('naturaleza_gym')
        medallas_gym = request.POST.get('medallas_gym')
        
        Gimnasio.objects.create(
            lider_id=lider, 
            naturaleza_gym=naturaleza_gym, 
            medallas_gym=medallas_gym
        )
        return redirect('gimnasios')
        
    return render(request, 'pokeapp/crear_gimnasio.html') 

def crear_entrenador(request):
    if request.method == 'POST':
        # Recoge los datos enviados por el formulario (ajusta los nombres según tus campos del modelo)
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        
        # Aquí guardas el objeto en la base de datos (importa tu modelo Entrenador si es necesario)
        # Entrenador.objects.create(nombre=nombre, edad=edad)
        
        return redirect('entrenadores')
        
    return render(request, 'pokeapp/crear_entrenador.html')