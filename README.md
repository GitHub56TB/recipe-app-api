### recipe-app-api
Recipe App API source code using Docker and Django

<https://www.markdownguide.org/basic-syntax#code>

#### Notes

git pull origin master --rebase

* Replace master branch in Git, entirely, from another branch
It’s for Newbie (Not recommended in production)
Let’s say you have two branches in my Git repository:
* 		master/main
* 		branch1 (created originally from master)
* Situation 1:
* 
 Couple of months ago and the code in this branch is 15 versions ahead of master
 
 or

* Situation 2:
 You messed up your master and you had initial copy with branch.
 
 Solution
    git checkout branch1
    git merge -s ours main
    git checkout main
    git merge branch1
    git push --force origin main

    The result should be your master/main is now essentially branch1.

   (-s ours is short for --strategy=ours)

#### Dockerfile
FROM python:3.10-alpine3.15
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN adduser -D user
USER user

#### docker-compose.yml
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
   
#### requirements.txt
Django>=4.0.4,<4.1.0
djangorestframework>=3.13.1,<3.14.0


xxx % docker-compose build
xxx % docker-compose run app django-admin startproject mysite . 
xxx % docker-compose up

need to add “app” directory first
xxx % docker-compose build
xxx % docker-compose run app django-admin startproject app . 
xxx % docker-compose up

xxx % docker-compose run app python manage.py startapp core 
xxx % docker-compose up



git push

recipe-app-api % docker-compose run app sh -c "python manage.py test" 
or
recipe-app-api % docker-compose run app python manage.py test 

Add flake to requirements.txt
recipe-app-api % python3 -m pip install flake8


recipe-app-api % docker-compose run app python manage.py test && flake8

git checkout temp/tng  

docker-compose run app python manage.py startapp core 
docker-compose run app python manage.py test

git checkout main

recipe-app-api % docker-compose run app python manage.py makemigrations core