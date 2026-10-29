from django.db import models

class Entrenadores(models.Model):
    id_documento = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    pokemones = models.CharField(max_length=100)
    medallas = models.IntegerField()

    def __str__(self):
        return f'{self.nombre} {self.apellido} (Doc: {self.id_documento})'


class Gimnasio(models.Model):
    lider_del_GYM = models.CharField(max_length=23)
    Naturaleza_de_GYM = models.CharField(max_length=24)
    Medallas = models.CharField(max_length=30, null=True, blank=True)  # <--- Agrega null y blank
    def __str__(self):
        return f'Gimnasio de {self.lider_del_GYM} - Tipo {self.Naturaleza_de_GYM}'


class Pokemon(models.Model):
    nombre = models.CharField(max_length=23)
    peso = models.FloatField()
    imagen = models.ImageField(upload_to='pokemons/', blank=True, null=True)
    
    # Cardinalidad: Un Entrenador tiene muchos Pokemones (ForeignKey)
    entrenador = models.ForeignKey(
        Entrenadores, 
        on_delete=models.CASCADE, 
        related_name='lista_pokemons', 
        blank=True, 
        null=True
    )
    
    habilidades = models.CharField(max_length=100)
    naturaleza = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombre} ({self.naturaleza})'