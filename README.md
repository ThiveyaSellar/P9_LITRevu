# P9_LITRevu

## Description du projet

La start-up LITRevu souhaite qu'une application web soit conçue pour permettre à ses utilisateurs de publier des critiques de livres ou d’articles et de consulter ou de demander une critique de livres.
Pour réaliser ce projet, on utilise Django qui est un framework Python.

## Installation

```
# Cloner le dépôt distant
$ git clone https://github.com/ThiveyaSellar/P9_LITRevu.git

# Créer un environnement virtuel
$ python -m venv env

# Activer l'environnement virtuel
- Linux :
$ source env/bin/activate
- Windows :
env\Scripts\activate.bat

# Installer les paquets nécessaires à partir du fichier requirements.txt
$ pip install -r requirements.txt

# Lancer le serveur
$ python manage.py runserver
```

## Administration

- Aller sur http://127.0.0.1:8000/admin
- S'authentifier si vous avez les droits d'accès pour accéder à l'interface d'administration django.

### Documentation Django

https://docs.djangoproject.com/en/4.2/

## Générer le rapport de flake 8

```
flake8
```