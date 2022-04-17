### recipeAPI Back-End Clean

SSH git@github.com:

…or create a new repository on the command line
echo "# apiback" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:
git push -u origin main

…or push an existing repository from the command line
git remote add origin git@github.com:
git branch -M main
git push -u origin main

HTTPS https://github.com/

…or create a new repository on the command line
echo "# apiback" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/
git push -u origin main

…or push an existing repository from the command line
git remote add origin https://github.com/
git branch -M main
git push -u origin main

=======================================
```
Dockerfile
FROM python:3.10-alpine3.15
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN adduser -D user
USER user

docker-compose.yml
version: "3"  # optional since v1.27.0
services:
  app:
    build: .
    volumes:
      - .:/django
    ports:
      - 8000:8000
    image: app:django
    container_name: django_container
    command: python manage.py runserver 0.0.0.0:8000
   
requirements.txt
Django>=4.0.4,<4.1.0
djangorestframework==3.13.1,<3.14.0
flake8>=4.0.1,<4.1.0

mkdir app

docker build .
docker-compose build

docker-compose run app django-admin startproject app . 
============
See UPDATE: Use GitHub Actions instead Below
============

calc.py
def add(x, y):
    """Add two numbers together and return the result"""
    return x + y

tests.py
from django.test import TestCase
from app.calc import add

class CalcTests(TestCase):
    def test_add_numbers(self):
        """Test that values are added together"""
        self.assertEqual(add(3, 8), 11)

docker-compose run app python manage.py test 
or
cd app/
python3 manage.py test 

tests.py (BEFORE)
from django.test import TestCase
from app.calc import add, subtract

class CalcTests(TestCase):

    def test_add_numbers(self):
        """Test that values are added together"""
        self.assertEqual(add(3, 8), 11)

    def test_subtract_numbers(self):
        """Test that values are subtracted and returned"""
        self.assertEqual(subtract(5, 11), 6)

python3 manage.py test 

calc.py (BEFORE)
def add(x, y):
    """Add two numbers together and return the result"""
    return x + y

def subtract(x, y):
    """Subtract x from y and return result"""
    pass
    # return (y - x)

python3 manage.py test && flake8

rename calc and tests (add x_ prefix)

python3 manage.py startapp core 

rename calc and tests (add x_ prefix) in core

create app/core/tests/__init__.py

add ‘core’, to settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',

create app/core/tests/test_models.py
test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
			email=email,
			password=password
		)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


python3 manage.py test && flake8

models.py (core)
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

add at end of settings AUTH_USER_MODEL = 'core.User'

python3 manage.py makemigrations core

python3 manage.py test
or
cd ..
docker-compose run app python manage.py test 
cd app/

add to test_models.py
def test_new_user_email_normalized(self):
	"""Test the email for a new user is normalized"""
	email = 'test@LONDONAPPDEV.com'
	user = get_user_model().objects.create_user(email, 'test123')
	
	self.assertEqual(user.email, email.lower())


replace line in models.py with
user = self.model(email=self.normalize_email(email), **extra_fields)

python3 manage.py test

add to test_models.py
def test_new_user_invalid_email(self):
    """Test creating user with no email raises error"""
    with self.assertRaises(ValueError):
        get_user_model().objects.create_user(None, 'test123')

replace l”create_user function in models.py with
def create_user(self, email, password=None, **extra_fields):
    """Creates and saves a new User"""
    if not email:
        raise ValueError('Users must have an email address')
    user = self.model(email=self.normalize_email(email), **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user

add to test_models.py
def test_new_superuser(self):
    """Test creating a new superuser"""
    user = get_user_model().objects.create_superuser(
        'test@londonappdev.com',
        'test123'
    )

    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)

add to test_models.py
def create_superuser(self, email, password):
    """Creates and saves a new super user"""
    user = self.create_user(email, password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user

=========
UPDATE: Use GitHub Actions instead
Travis-CI no longer offers a free tier and we are working on a course update which uses GitHub Actions instead.
In the meantime, here are the steps for setting up GitHub Actions.
1. Register on Docker Hub
If you don't already have one, head over to hub.docker.com and register for a new free account.
Under Account Settings > Security, create a new Access Token.
2. Add credentials to your GitHub Repo
Open your repo on GitHub and select Settings:
```