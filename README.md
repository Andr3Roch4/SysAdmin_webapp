# M6 - Projeto 1 - WebApp

Este projeto teve como objetivos: 1- Criação de uma API REST para a aplicação desenvolvida no primeiro projeto do módulo anterior e 2- Alojamento dessa API numa máquina virtual (VM) Azure. De seguida, apresenta-se um guia de como atingir o segundo objetivo, utilizando a API presente neste repositório, a qual foi desenvolvida com Django.

## Infraestrutura necessária

1. Rede Virtual Azure (VNET)

2. VM, com os seguintes requisitos mínimos:

    vCPU: 1
    RAM: 1GB
    SO: Ubuntu
    Disco: Tamanho mínimo para o SO(32GB)

3. Software: 
    - git (pré-instalado nas VMs Azure)
    - cifs-utils (pré-instalado nas VMs Azure)
    - python3 (pré-instalado nas VMs Azure)
    - pip

4. Conta de Armazenamento

## Criação da Rede Virtual (VNet)
1. Aceder ao recurso "Redes Virtuais", "Criar" uma nova VNet

2. Em "Informações Básicas", preencher todos os campos

3. Selecionar "Rever + criar" e verificar se as informações estão corretas para criar a nova VNet

## Criação da Máquina Virtual

1. Aceder ao recurso Máquinas Virtuais, opção criar nova Máquina Virtual do Azure.

    - subscrição: FCUL-UPSKILL
    - Grupo de recursos: RG-UPSKILL-SysAdmin 
    - Região: Spain Central
    - Imagem: Linux (ubuntu 24.04)
    - Tamanho: Standard B1ms (1 vcpu, 2 GiB memória)
 2. Nas definições de disco, selecionar o tipo e tamanho do disco para armazanemto do S.O.

    - Tipo: LRS HDD Standard
    - Tamanho: 32 GiB
 3. Nas definições de rede, em interface de rede, selecionar a VNet criada anteriormente.  

4. Depois de criada a VM, nas definições de rede, é necessário definir as regras de entrada de portas usadas pela webapp (8000).

## Criação da Conta de Armazenamento

1. Durante a criação da conta de armazenamento selecionar:
    
    - subscrição: FCUL-UPSKILL
    - Grupo de recursos: RG-UPSKILL-SysAdmin
    - Região: Spain Central

2. Criação de uma pasta partilhada com a base de dados da nossa aplicação

## Guia de instalação da aplicação API

1. Aceder à VM por ssh
```
ssh <username>@<ip_publico_VM>
```

2. Atualizar lista de pacotes apt
``` 
sudo apt update
```

3. Instalar o gestor de pactores ``pip``
``` 
sudo apt install pip
```

4. Clonar o repositório com a API REST
``` 
git clone https://gitlab.com/lezz-git-it/webapp.git
```

5. Navegar até à pasta ``webapp``
```
cd webapp
```

6. Criar um ambiente virtual e instalar os requisitos no mesmo

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

7. Criar o ficheiro com as credenciais da conta de armazenamento onde se encontra o ficheiro da base de dados
```
sudo nano /etc/azurefiles.cred
```
```
username=[nome da conta de armazenamento]
password=[chave da conta de armazenamento]
```
8. Criar o diretório ``db`` dentro do diretório ``webapp``:

9. Para que a pasta da base de dados seja montada na pasta da webapp, a cada boot, editar o ficheiro ``/etc/fstab``, acrescentando a seguinte linha no final:
```
sudo nano /etc/fstab
```
```
//<nome_conta_armazenamento>.file.core.windows.net/<nome_conta_armazenamento>/<nome_pasta_partilhada> /home/<username>/webapp/db cifs credentials=/etc/azurefiles.cred,vers=3.0,serverino,dir_mode=0777,file_mode=0777,nobrl 0 0
```

10. Para aplicar as alterações sem ter de reiniciar a VM:
```
systemctl daemon-reload
```
(Aqui terá de introduzir a palavra-passe de utilizador da VM)
```
sudo mount -a
```

11. Mudar para o branch ``production``
```
git checkout production
```

12. Adicionar o IP da VM à lista de allowed_hosts da aplicação
```
nano webapp/settings.py
```

13. Correr o servidor
```
python manage.py runserver 0.0.0.0:8000
```

## Calculo de Custos usado

| Service category | Service type      | Custom name | Region         | Description                                                                                                                                                                                                 | Estimated monthly cost |
|------------------|-------------------|-------------|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|
| Calcular         | Virtual Machines  |             | Spain Central  | 1 B1ms (1 Core, 2 GB RAM) x 730 Horas (Pay as you go), Linux, (Pay as you go); 1 managed disk – S4; Inter Region transfer type, 5 GB outbound data transfer from Espanha Central to Leste da Ásia            | €16,90                 |
| Calcular         | App Service       |             | Spain Central  | Camada Gratuito; 1 (0 núcleos, 0 GB de RAM, 0 GB de armazenamento) x 730 Horas; Linux SO                                                                                                                    | €0,00                  |
| Armazenamento    | Storage Accounts  |             | Spain Central  | Redundância Armazenamento de Blobs de Bloco, Uso geral V2, Namespace simples, LRS, Quente Camada de Acesso, Capacidade de 6 GB - PAGO CONFORME O USO, 1 x 10.000 operações de Gravação, 1 x 10.000 Operações de Lista e Criação de Contêiner, 2 x 10.000 operações de Leitura, 1 x 10.000 Outras operações. 1.000 GB Recuperação de Dados, 1.000 GB Gravação de Dados, SFTP desabilitado | €0,21                  |
|                  |                   | Total        |                |                                                                                                                                                                                                             | €17,12                 |



## Contributors:
- André Rocha
- Pedro Pires
- Waltenberg Dantas