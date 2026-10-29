from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Pokemon
from .forms import PokemonForm

# Vista principal del catálogo con barra de búsqueda integrada
def index(request):
    query = request.GET.get('q', '')
    if query:
        pokemons = Pokemon.objects.filter(nombre__icontains=query)
    else:
        pokemons = Pokemon.objects.all()
        
    return render(request, 'pokeapp/index.html', {'pokemons': pokemons, 'query': query})

# Vista de detalles de un Pokémon
def detalle_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    return render(request, 'pokeapp/detalle.html', {'pokemon': pokemon})

# Vista personalizada de Inicio de Sesión
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

# Vista para registrar un nuevo Pokémon (Protegida)
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

# Vista para editar un Pokémon existente (Protegida)
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

# Vista para eliminar un Pokémon (Protegida)
@login_required(login_url='/accounts/login/')
def eliminar_pokemon(request, pk):
    pokemon = get_object_or_404(Pokemon, pk=pk)
    if request.method == 'POST':
        pokemon.delete()
        return redirect('index')
    return render(request, 'pokeapp/eliminar_pokemon.html', {'pokemon': pokemon})