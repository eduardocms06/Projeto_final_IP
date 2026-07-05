GUIA DE INSTALAÇÃO:

#1 Instale o OLLAMA
https://ollama.com/download

#2 Verifique se intalou corretamente abrindo o cmd e digitando:
ollama --version
Se aparecer uma versão, tipo: ollama version 0.x.x 
Então deu certo!

#3 Escreva no cmd e baixe a versão 2.3 do llama:
ollama pull llama3.2

## Estrutura do Projeto

```
.
├── Projeto_final_IP
    ├── agentes
        └── investigador.py         #Arquivo que busca se a resposta é valida dentro do banco de dados .json
        └── respondedor.py          # Ainda não está completo com o RAG
    ├── dados
        ├── animais 
            └── nome animal.json...         #Contém 1 arquivo json para cada animal incluido no arquivo
        ├── caracteristicas
            └── caracteristicasAnimais.json         #Dicionário de perguntas para cada uma das características
    ├── Frontend
        ├──estatic
            └──CSS          #Todo o estilo de página.
            └──HTML         #estrutura do texto das 3 telas, HOME, MODALIDADES, CHAT
            └──JavaScript       #Utilizado para navegação e comportamento visual da aplicação
    ├── rag
        └── consulta. py              #Incompleto, ainda falta a implementação
        └── indexador.py              #Incompleto, ainda falta a implementação
        └──rag_app.py                  #estrutura base do RAG
    ├── utils
        └──carregador .py              #carrega todos os bancos de dados
    ├──main.py                         #arquivo principal
    ├── README.md
```
## Telas

1. Home - Contém título do jogo
    `Botões modalidades` - entra na 2º pag 
    - `sair` - Dispara alguns sinais no terminal para finalizar a aplicação
2. Modalidades - Contém uma grade com 4 botões modalidades
3. Chat - Onde irá ocorrer toda a conversa com RAG ou Banco de dados.

## Acessibilidade e responsividade
- Responsivo para telas até 560px

## Banco de dados
- Características animais - Armazena dicionario para perguntas de sim ou não para cada característica dos animais
- animais Adiciona cada caractteristica a seu respectivo animal

## MOTOR RAG
- Incompleto, falta implementação e criação de funções para as perguntas e respostsa do RAG
