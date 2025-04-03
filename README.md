# M6 - Projeto 1 - WebApp

(introdução)

## Infraestrutura necessária
1- Possuir VNET

2- Possuir VM, com os seguintes requisitos mínimos:

    vCPU: 1
    RAM: 1GB
    SO: Ubuntu
    Disco: Tamanho mínimo para o SO(32GB)

    Software: 
    - git (pré-instalado nas VMs Azure)
    - python3 (pré-instalado nas VMs Azure)
    - pip

## Criação da Rede Virtual
1- Aceder ao recurso "Redes Virtuais"

2- Carregar em "Criar"

3- Em "Informações Básicas", preencher todos os campos

4- Carregar em "Rever + criar" e verificar se as informações estão corretas

5- Carregar em "Criar"

## Criação da Máquina Virtual

1- ...

6- Abrir portas

## Guia de instalação da aplicação API

1- Aceder à VM por ssh
```
ssh <username>@<ip_publico_VM>
```

2- Atualizar lista de pacotes apt
``` 
sudo apt update
```

3- Instalar o gestor de pactores ``pip``
``` 
sudo apt install pip
```

4- Clonar o repositório com a API REST
``` 
git clone https://gitlab.com/lezz-git-it/webapp.git
```

5- Navegar até à pasta ``webapp``
```
cd webapp
```

6- Criar um ambiente virtual e instalar os requisitos no mesmo

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

7- Criar o ficheiro com as credenciais da conta de armazenamento onde se encontra o ficheiro da base de dados
```
sudo nano /etc/azurefiles.cred
```
```
username= [nome da conta de armazenamento]
password= [chave da conta de armazenamento]
```
8- Criar a pasta ``db``

9- Para que a pasta da base de dados seja montada na pasta da webapp, a cada boot, editar o ficheiro ``/etc/fstab``, acrescentando a seguinte linha no final:
```
//<nome_conta_armazenamento>.file.core.windows.net/<nome_conta_armazenamento>/db /home/<username>/webapp/db cifs credentials=/etc/azurefiles.cred,vers=3.0,serverino,dir_mode=0777,file_mode=0777,nobrl 0 0
```
(nobrl - Disables byte-range locking (required for SQLite over SMB))

10- Para aplicar as alterações sem ter de reiniciar a VM:
```
systemctl daemon-reload
```
```
sudo mount -a
```

11- Mudar para o branch production
```
git checkout production
```

12- Adicionar o IP da VM à lista de allowed_hosts da aplicação
```
nano webapp/settings.py
```


13- Correr o servidor
```
python manage.py runserver 0.0.0.0:8000
```


## Histórico de comandos usados
```
django-admin startproject webapp .
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






## Contributors:
- André Rocha
- Pedro Pires
- Waltenberg Dantas