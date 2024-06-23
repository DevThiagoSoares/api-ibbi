# API Desafio IBBI

Api feita com Fastapi (python) para controle de vendas de um e-commerce.

## 🚀 Começando

O projeto pode ser startado de 2 maneiras, localmente ou via docker.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.

### 📋 Pré-requisitos
Certifique-se de ter Python e pip instalados. Recomenda-se usar um ambiente virtual para isolar as dependências do projeto.
```
sudo apt update
sudo apt install python3
```
Verifique sua versão do python
```
python3 --version
```

```
sudo apt install python3-pip
```
Verifique sua versão do python
```
pip3 --version
```
Se estiver no windows acesse o site oficial do Python em python.org e baixe o instalador da versão mais recente do Python. Escolha o instalador adequado para o seu sistema (32-bit ou 64-bit). 

### 🔧 Instalação e Execução
Após a configuração do ambiente podemos iniciar a aplicação instalando os dependencias necessárias para rodar a aplicação.

```
pip install -r requirements.txt
```

Para rodar localmente mude o valor dá variavel de ambiente POSTGRES_HOST para `localhost`, caso for subir com docker compose deve permanecer `postgres-db` ou o nome de seu cointainer do postgres.
```
python3 -u main.py
```
Caso queria rodar com o uvicorn

```
uvicorn main:app --port 8003 --reload
```

## 🛠️ Construído com

* [Fastapi](https://fastapi.tiangolo.com/) - O framework python usado
* [SQLalchemy](https://www.sqlalchemy.org/) - ORM de banco de dados
* [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Usada para gerar migrations
* [Docker](https://www.docker.com/) - Plataforma para desenvolvimento, envio e execução de aplicações em contêineres
* [Docker Compose](https://docs.docker.com/compose/) - Ferramenta para definir e gerenciar aplicações Docker multi-contêiner

## 🌐 Acessar em produção 

## 

