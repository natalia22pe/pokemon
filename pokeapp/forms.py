from django import forms
from .models import Pokemon  

class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['nombre', 'peso', 'imagen']  # Los campos de tu base de datos que el usuario podrá llenar
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ingresa el nombre del Pokémon'
            }),
            'peso': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej. 6.5'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }