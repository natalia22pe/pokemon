from django import forms
from .models import Pokemon, Entrenadores, Gimnasio

class PokemonForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['nombre', 'peso', 'imagen', 'nivel', 'habilidades', 'naturaleza', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nivel': forms.NumberInput(attrs={'class': 'form-control'}),
            'habilidades': forms.TextInput(attrs={'class': 'form-control'}),
            'naturaleza': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = Entrenadores
        fields = ['id_documento', 'nombre', 'apellido', 'medallas', 'pokemones']
        widgets = {
            'id_documento': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'medallas': forms.NumberInput(attrs={'class': 'form-control'}),
            'pokemones': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

class GimnasioForm(forms.ModelForm):
    class Meta:
        model = Gimnasio
        fields = ['lider', 'naturaleza_gym', 'medallas_gym']
        widgets = {
            'lider': forms.Select(attrs={'class': 'form-control'}),
            'naturaleza_gym': forms.TextInput(attrs={'class': 'form-control'}),
            'medallas_gym': forms.TextInput(attrs={'class': 'form-control'}),
        }