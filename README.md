# P9_LITRevu

## Description du projet

La start-up LITRevu souhaite qu'une application web soit conçue pour permettre à ses utilisateurs de publier des critiques de livres ou d’articles et de consulter ou de demander une critique de livres.
Pour réaliser ce projet, on utilise Django qui est un framework Python.

## Installation


- Cloner le dépôt distant :

```
$ git clone https://github.com/ThiveyaSellar/P9_LITRevu.git
```

- Créer un environnement virtuel :
```
$ python -m venv env
```

- Activer l'environnement virtuel :
- Linux :
```
$ source env/bin/activate
```
- Windows :
```
env\Scripts\activate.bat
```

- Installer les paquets nécessaires à partir du fichier requirements.txt :
```
$ pip install -r requirements.txt
```
- Lancer le serveur local :
```
$ python manage.py runserver
```
- Ouvrir l'application web dans un navigateur :
http://127.0.0.1:8000/

## Administration

Pour accéder à l'interface d'administration de Django il faut être un super utilisateur.

- Créer un superuser :
```
$ python manage.py createsuperuser
```
- Lancer le serveur local :
```
$ python manage.py runserver
```
- Aller sur http://127.0.0.1:8000/admin et s'authentifier si vous êtes un super utilisateur.

# Flake8

Flake8 est un paquet qui permet de vérifier que le code respecte les directives PEP8.
- Fichier de configuration : tox.ini
- Générer le rapport de flake 8 :
```
$ flake8
```