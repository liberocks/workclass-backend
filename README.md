# How to start django

```py
# install deps
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

# How to start django with docker

```bash
docker build . -t workclass-backend
docker run --name workclass-backend-container -d -p 8000:8000 workclass-backend
```