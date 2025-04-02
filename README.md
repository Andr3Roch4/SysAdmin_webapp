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

##### Necessário usar cifs-utils para montar a base de dados que esta no Azure Files

```
sudo apt install cifs-utils
```

```
sudo mkdir db
```

```
sudo mount -t cifs //formando30.file.core.windows.net/formando30/db/ /home/upskill/webapp/db -o vers=3.0,username=formando30,password=7jzpvEzxYX/DxCdSSbguaT4U2ex/7j9IQViKMqrTJh09bQOXg
FJQ+St6TyDQP+EynPwe8yl640Q7+ASt+LI+gQ==,dir_mode=0777,file_mode=0777,serverino,nobrl
```

```
//formando30.file.core.windows.net/formando30/db /home/upskill/webapp/db cifs credentials=/etc/azurefiles.cred,vers=3.0,serverino,dir_mode=0777,file_mode=0777,nobrl 0 0
```

```
systemctl daemon-reload
```

```
sudo mount -o remount /home/upskill/webapp/db
```

```
sudo nano /etc/azurefiles.cred
```