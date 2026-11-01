from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Entrenadores(models.Model):
    id_documento = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    medallas = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(20)])
    
    # Relación Muchos a Muchos (N:M) con Pokemon
    pokemones = models.ManyToManyField('Pokemon', related_name='entrenadores', blank=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido} (Doc: {self.id_documento})'


class Gimnasio(models.Model):
    # Relación con Entrenadores: Un entrenador específico es el líder de este gimnasio
    lider = models.ForeignKey(Entrenadores, on_delete=models.SET_NULL, null=True, blank=True, related_name='gimnasio_liderado')
    naturaleza_gym = models.CharField(max_length=50)
    medallas_gym = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        lider_nombre = f"{self.lider.nombre} {self.lider.apellido}" if self.lider else "Sin líder asignado"
        return f'Gimnasio de {lider_nombre} - Tipo: {self.naturaleza_gym}'


class Pokemon(models.Model):
    nombre = models.CharField(max_length=50)
    peso = models.FloatField(validators=[MinValueValidator(0.1)])
    imagen = models.ImageField(upload_to='pokemons/', blank=True, null=True)
    nivel = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    habilidades = models.CharField(max_length=100)
    naturaleza = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre} ({self.naturaleza})'
