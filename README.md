
### 1. Pré-requisitos para rodar a aplicação (Ollama)
O projeto utiliza um modelo de linguagem local. Siga os passos abaixo:
1. Baixe e instale o [Ollama](https://ollama.com/download).
2. Verifique se a instalação foi concluída com sucesso abrindo o terminal (cmd) e digitando:
```bash
   ollama --version
```
3. Novamente no CMD baixe a versão 2.3 do Ollama digitando:
```bash
   ollama pull llama3.2
```
### 2. Rodando o projeto
Com o Ollama configurado clone este repositório e instale as dependências.
```bash
# Crie e ative um ambiente virtual na máquina (Opcional, porém recomendado).
python -m venv .venv

#Para ativar no Mac/Linux
source .venv/bin/activate

#Para ativar no windows
.venv\Scripts\activate
```
1. Próximo Passo Instale as dependências
```bash
pip install -r requirements.txt
```
2. Rode a aplicação
```bash
python main.py
```



## Estrutura do Projeto

```
.
Projeto_final_IP/
├── .venv/                          # Ambiente Virtual (configurações locais)
├── chroma_db                       #Banco de dados vetorial (Gerado automaticamente)
├── data/                           # Arquivos de dados (.json, CSV, etc.)
|   └── animais/                    # Dicionário de cada animal com sua característica
|   └── características/            # Dicionário de perguntas e características dos animais
├── src/                            # Todo o código fonte do projeto
|   └── agentes/                    # Módulos para a construção dos agentes
|   └──jogo/                        # Lógica central do jogo (regras, jogadores e partida)
|   └──llm/                         # Interpretação e integração com o modelo local
|   └── rag/                        # Módulos do motor RAG
|   └── templates/                  # Arquivos de templates (HTML, CSS, Js, etc.)
|   └── utils/                      # Funções de utilizdades e códigos auxiliares
├── testes/                         # Scripts de testes (ex: teste_partida)
├── .gitignore                      # Arquivos que devem ser ignorados
├── app.py                          # Arquivo para execução de todos os métodos e Front-End + Back-End
├── main.py                         # Arquivo de execução principal
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
