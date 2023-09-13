from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Nom d'utilisateur"
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput,
        label="Mot de passe"
    )

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Obtenir le modèle User sans l'importer avec get_user_model
        model = get_user_model()
