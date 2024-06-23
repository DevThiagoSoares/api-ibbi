# API Desafio IBBI

Api feita com Fastapi (python) para controle de vendas de um e-commerce.

# 🌐 Acessar em Produção

## 🚀 [IBBI Desadio](https://ibbi-ui.vercel.app)


Acesse a aplicação de produção clicando no link acima. Este é o ambiente principal onde você pode ver todas as funcionalidades do projeto em ação.

> **Nota:** Certifique-se de revisar todas as funcionalidades e fornecer feedback. Sua opinião é crucial para a melhoria.

---
---

O projeto pode ser startado de 2 maneiras, localmente ou via docker.

## 🚀 Começando

### 📋 Requisitos para Docker
- Docker: Certifique-se de que o Docker está instalado e em execução.
- Docker Compose: Verifique se o Docker Compose está instalado.

Isso conclui as instruções para executar o projeto com Docker e os pré-requisitos necessários.

### 🐳 Rodar com Docker
Para rodar o projeto com Docker, siga os passos abaixo:

1. **Certifique-se de ter o Docker e o Docker Compose instalados.** Se não tiver, siga as instruções de instalação no site oficial do Docker: [Instalação do Docker](https://docs.docker.com/get-docker/)

2. **Construa e inicie os containers com Docker Compose:**
    ```
    docker-compose up --build
    ```

3. **Acesse a aplicação:**
   A aplicação estará disponível em `http://localhost:8003`.


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

## 🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir um problema ou enviar uma solicitação de pull.

## 📧 Contato
Se você tiver alguma dúvida, entre em contato pelo e-mail: devthiagosoares@gamil.com
