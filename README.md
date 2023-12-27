# P9_LITRevu

## About this project

The start-up LITRevu wants a web application designed to enable its users to publish reviews of books or articles, and to consult or request book reviews.
To realize this project, we're using Django, a Python framework.

## Installation


- Clone remote repository :

```
git clone https://github.com/ThiveyaSellar/P9_LITRevu.git
```

- Create a virtual environment in the project :
```
python -m venv env
```

- Activate virtual environment :
- Linux :
```
source env/bin/activate
```
- Windows :
```
env\Scripts\activate.bat
```

- Install the necessary packages from requirements.txt :
```
pip install -r requirements.txt
```
- Go to the litrevu directory and launch the local server :
```
python manage.py runserver
```
- Open the web application in a browser :
http://127.0.0.1:8000/

## Administration

To access Django's administration interface, you need to be a superuser.

- Create a superuser :
```
python manage.py createsuperuser
```
- Start the local server :
```
python manage.py runserver
```
- Go to http://127.0.0.1:8000/admin and log in if you are a superuser.

# Flake8

Flake8 is a package for checking that code complies with PEP8 guidelines.
- Configuration file : tox.ini
- Generate flake 8 report :
```
flake8
```