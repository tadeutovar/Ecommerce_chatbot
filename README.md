# 🛍️ Ecommerce Chatbot

## 📋 Descrição

Este projeto é um **chatbot inteligente** desenvolvido em Python que interage com uma API de e-commerce para permitir ao usuário:

- Consultar **produtos disponíveis**;
- Visualizar seus **pedidos anteriores** com base no e-mail;
- Acessar um **extrato de cartões** vinculados ao seu usuário;
- Encerrar a sessão com o comando sair.

O foco está em comandos simples, linguagem natural e integração com uma API real hospedada na nuvem.

---

## 🚀 Tecnologias Utilizadas

- **Python** – Linguagem principal do projeto.
- **[BotBuilder SDK (Microsoft)](https://github.com/microsoft/botbuilder-python)** – Framework para criação de chatbots.
- **httpx** – Cliente HTTP assíncrono para chamadas à API REST.
- **FastAPI** – Backend da API (já hospedado no Azure).
- **Azure App Service** – Hospedagem da API.
- **Azure Cosmos DB e MySQL** – Bancos de dados utilizados no backend.

---

## 💡 Funcionalidades

- 🔐 **Login via e-mail**: o bot verifica se o e-mail informado está associado a pedidos anteriores.
- 🛒 **Consulta de produtos**: mostra todos os produtos cadastrados.
- 📦 **Consulta de pedidos**: retorna os pedidos do usuário com informações de data, status e valor.
- 💳 **Consulta de cartões (extrato)**: mostra os cartões vinculados ao usuário, com número, validade e saldo.
- 🚪 **Logout**: o comando `sair` limpa o e-mail e encerra a sessão do usuário.

---

## 🧪 Como Rodar Localmente

1. Clone o repositório:

bash
git clone https://github.com/seu-usuario/ecommerce-chatbot.git
cd ecommerce-chatbot
Crie um ambiente virtual e instale as dependências:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
Execute o bot com um adaptador apropriado (ex: console ou Web Chat).

⚠️ Certifique-se de que a variável API_BASE_URL no código esteja apontando corretamente para o endpoint da API hospedada.

## 🧠 Exemplo de Interação

Você: tadeu@example.com  
Bot: ✅ Login realizado com sucesso como **tadeu@example.com**!

Você pode digitar:
- produtos
- pedidos
- extrato
- sair

Você: produtos  
Bot: 🛒 Produtos disponíveis:
- Camisa Polo — R$ 99.90
- Tênis Running — R$ 279.90

Você: extrato  
Bot: 💳 Cartões vinculados:
- Número: ****5678
  Validade: 12/26
  Saldo: R$ 9400.20

- Número: ****4111
  Validade: 04/30
  Saldo: R$ 1500.00
  
## 📚 Projeto Acadêmico
Este projeto foi desenvolvido como parte da disciplina Big Data e Cloud Computing do curso de Ciência de Dados e Inteligência Artificial no Ibmec.

## 👥 Grupo
Tadeu Tovar
Marcelo Saggio
Lucas Goulart
Bernardo Moreira

