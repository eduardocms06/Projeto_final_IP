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
Projeto_final_IP/
├── .venv/                          # Ambiente Virtual (configurações locais)
├── assets/                         # Imagens, mídias e outros recursos visuais
├── data/                           # Arquivos de dados (.json, CSV, etc.)
|   └── animais/                    # Dicionário de cada animal com sua característica
|   └── características/            # Dicionário de perguntas e características dos animais
├── src/                            # Todo o código fonte do projeto
|   └── agentes/                    # Módulos para a construção dos agentes
|   └── rag/                        # Módulos do motor RAG
|   └── templates/                  # Arquivos de templates (HTML, CSS, Js, etc.)
|   └── utils/                      # Funções de utilizdades e códigos auxiliares
|
├── .gitignore                      # Arquivos que devem ser ignorados
├── main.py                         # Arquivo principal de toda a aplicação
├── README.md                       # Documentação principal do projeto
├── requirements.txt                # Lista dos materiais que são necessários para o bom funcionamento do projeto.
```
## Telas

1. Home - Contém título do jogo
    `Botões modalidades` - entra na 2º pag 
    - `sair` - Dispara alguns sinais no terminal para finalizar a aplicação
2. Modalidades - Contém uma grade com 4 botões modalidades
3. Chat - Onde irá ocorrer toda a conversa com RAG ou Banco de dados.

## Acessibilidade e responsividade
- Responsivo para telas até 560px

## Dependências externas
- Fontes do Google Fonts: Special Elite e Share Tech Mono, carregadas via <link> no index.html. Para uso totalmente offline, baixe as fontes e sirva localmente.

## Banco de dados
- Características animais - Armazena dicionario para perguntas de sim ou não para cada característica dos animais
- animais Adiciona cada caractteristica a seu respectivo animal

## MOTOR RAG
- Incompleto, falta implementação e criação de funções para as perguntas e respostsa do RAG
