from django import forms
from .models import Equipment
from django.contrib.auth.models import User
from .models import Utilisateur
from .models import admin

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['id', 'serial_code', 'name', 'type', 'equipment', 'brand', 'purchase_date', 'statut', 'user']
        widgets = {
            'purchase_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'type': forms.Select(attrs={'id': 'type'}),
            'equipment': forms.Select(attrs={'id': 'equipment'}),
            'statut': forms.Select(choices=[('En Service', 'En Service'), ('En Réparation', 'En Réparation')]),
        }

    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].choices = []  # Start with empty equipment choices


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['id', 'nom', 'prenom', 'role', 'email', 'equipement_id', 'date_debut','date_fin']
        widgets = {
            'date_debut': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
             'date_fin': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
            
        }


class AdminForm(forms.ModelForm):
    class Meta:
        model = admin
        fields =  ['id', 'nom', 'prenom', 'role', 'email', 'equipement_id', 'date_debut','date_fin']
        widgets = {
            'date_debut': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
             'date_fin': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date'}),
            
        }

    

