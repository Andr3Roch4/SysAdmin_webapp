# M6 - Projeto 1 - WebApp

Este projeto teve como objetivos: 1- Criação de uma API REST para a aplicação desenvolvida no primeiro projeto do módulo anterior e 2- Alojamento dessa API numa máquina virtual (VM) Azure. De seguida, apresenta-se um guia de como atingir o segundo objetivo, utilizando a API presente neste repositório, a qual foi desenvolvida com Django.

## Infraestrutura necessária

1- Rede Virtual Azure (VNET)

2- VM, com os seguintes requisitos mínimos:

    vCPU: 1
    RAM: 1GB
    SO: Ubuntu
    Disco: Tamanho mínimo para o SO(32GB)

    Software: 
    - git (pré-instalado nas VMs Azure)
    - cifs-utils (pré-instalado nas VMs Azure)
    - python3 (pré-instalado nas VMs Azure)
    - pip

## Criação da Rede Virtual
1- Aceder ao recurso "Redes Virtuais"

2- Carregar em "Criar"

3- Em "Informações Básicas", preencher todos os campos

4- Carregar em "Rever + criar" e verificar se as informações estão corretas

5- Carregar em "Criar"

## Criação da Máquina Virtual

1- Aceder ao recurso Máquinas Virtuais, opção criar nova Máquina Virtual do Azure.

 - Nas informações básicas preencher os campos obrigatórios na configuração da instância, como por exemplo:
    - subscrição: FCUL-UPSKILL
    - Grupo de recursos: RG-UPSKILL-SysAdmin 
    - Região: Spain Central (Zona 3)
    - Imagem: Linux (ubuntu 24.04)
    - Tamanho: Standard B1ms (1 vcpu, 2 GiB memória)
 - Nas definições de disco, selecionar o tipo e tamanho do disco para armazanemto do S.O.
    - Tipo: LRS HDD Standard
    - Tamanho: 32 GiB
 - Nas definições de rede, em interface de rede, selecionar a VNet criada anteriormente.  

2- Abrir as portas

- Nas definições de rede dentro da VM, é preciso definir as regras de entrada e saída de portas.

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
username=[nome da conta de armazenamento]
password=[chave da conta de armazenamento]
```
8- Criar o diretório ``db`` dentro do diretório ``webapp``:

9- Para que a pasta da base de dados seja montada na pasta da webapp, a cada boot, editar o ficheiro ``/etc/fstab``, acrescentando a seguinte linha no final:
```
sudo nano /etc/fstab
```
```
//<nome_conta_armazenamento>.file.core.windows.net/<nome_conta_armazenamento>/db /home/<username>/webapp/db cifs credentials=/etc/azurefiles.cred,vers=3.0,serverino,dir_mode=0777,file_mode=0777,nobrl 0 0
```
(nobrl - Disables byte-range locking (required for SQLite over SMB))

10- Para aplicar as alterações sem ter de reiniciar a VM:

```
systemctl daemon-reload
```
(Aqui terá de introduzir a palavra-passe de utilizador da VM)
```
sudo mount -a
```

11- Mudar para o branch ``production``
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

## Contributors:
- André Rocha
- Pedro Pires
- Waltenberg Dantas