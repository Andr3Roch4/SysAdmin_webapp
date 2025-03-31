# WebApp

## Histórico de comandos usados

```
python3 -m venv .venv
source .venv/bin/activate
pip install django
```

```
django-admin startproject webapp .
```

```
python manage.py runserver
```

```
python manage.py startapp cadeialogistica
```

##### Começar a escrever as views (cadeialogistica/views.py)

##### Começar a escrever os urls (cadeialogistica/urls.py)

##### Incluir novos caminhos (urls) da cadeialogistica na webapp

##### Incluir app cadeialogistica nas settings.py -> installed_apps

##### Incluir hostname nos allowed_hosts

```
az webapp up --runtime PYTHON:3.12 --name clogistica --sku B1 --logs --resource-group RG-UPSKILL-SysAdmin
```