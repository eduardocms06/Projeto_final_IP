# QUEM SOU EU?
- A aplicação a seguir trata de uma releitura do famoso jogo `Quem Sou Eu?`, onde o humano e a máquina participam de um duelo. Cada participante terá a sua chance de jogar e traçar perguntas estratégicas para descobrir quem consegue adivinhar primeiro o animal ou personagem do oponente. O jogo é composto por rodadas intercaladas, de perguntas e respostas de Sim ou Não, vai encarar o desafio?


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
2. Rode a aplicação utilizando: 
```bash
python app.py
```

## Estrutura do Projeto

```

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
## Front-End e Interface
* A camada de visualização e interação do jogo foi desenvolvida utilizando **JavaScript**, HTML5 e CSS3. A arquitetura foi projetada para ser leve, responsiva e dispensando a necessidade de *frameworks* externos para garantir o máximo de performance e carregamento instantâneo no navegador.
* A interface simula um ambiente de chat, onde o usuário interage diretamente com o agente de IA.

### Principais características
- **Comportamento de *Single Page Application*:** A navegação entre telas (seleção de modalidades, chat e fim de jogo) e a atualização dos painéis ocorrem de forma fluida e dinâmica, sem qualquer recarregamento de página.

- **Comunicação Assíncrona:** O front-end se comunica com o motor da IA e o backend através da API nativa `fetch` do navegador. O uso intensivo de requisições assíncronas (`async/await`) garante que a interface não congele enquanto o RAG e o Llama processam as jogadas.

- **Gerenciamento de Estado Local:** Variáveis de estado gerenciam o fluxo de turnos (Investigador vs. Respondedor), histórico de perguntas recentes e contextos de espera como por exemplo, aguardar o raciocínio da IA.

- **Renderização Dinâmica** Componentes visuais como, balões de mensagens, rótulos de sistema e botões de confirmação de palpite são construídos e inseridos dinamicamente na árvore do *Document Object Model* conforme a progressão da partida, fornecendo um *feedback* visual imediato ao jogador.

- **Tratamento de Erros e Resiliência:** Todo o fluxo de requisições está encapsulado em blocos seguros (`try/catch`). Em caso de latência ou falhas de rede, o sistema emite *feedbacks* e bloqueia interações duplicadas (*Double-Submit*) e previne travamentos silenciosos da interface.

## Dependências externas
- Fontes do Google Fonts: Special Elite e Share Tech Mono, carregadas via <link> no index.html. Para uso totalmente offline, baixe as fontes e sirva localmente.

## Banco de dados
- Características animais - Armazena dicionario para perguntas de sim ou não para cada característica dos animais
- animais Adiciona cada caractteristica a seu respectivo animal

## MOTOR RAG (Retrieval-Augmented Generation)
- O motor **RAG** é o componente responsável por unir o Llama com a interface de perguntas e respostas do projeto. Em vez de depender dos pesos pré-treinados do modelo básico, o sistema realiza consultas dinâmicas a uma base de dados que fornece o contexto semântico exato necessário a cada rodada da partida.

### Fulxo de Funcionamento
1. **Ingestão de Dados:** As características e os atributos de cada animal estão estruturados em arquivos `.JSON`.
2. **Vetorização (Embeddings):** Esses arquivos são processados e convertidos em vetores de alta dimensionalidade (*embeddings*), que representam matematicamente o significado semântico das propriedades de cada entidade.
3. **Persistência Vetorial (ChromaDB):** Os vetores resultantes são fixados e armazenados no **ChromaDB**.
4. **Recuperação e Contextualização:** A cada interação do jogador, o motor RAG realiza uma busca de similaridade no ChromaDB. Os fragmentos de dados mais relevantes ao contexto atual são recuperados e enviado ao modelo Llama.

### Benefícios do RAG
* **Processamento de Linguagem Natural Dinâmico:** Capacita o modelo a interpretar perguntas livres feitas pelo usuário e compreender respostas que fujam das determinações de (sim/não).
* **Evita Alucinações:** Restringe as respostas e o raciocínio lógico da IA à base de conhecimento integrada ao jogo, garantindo respostas consistentes de acordo com o banco de dados interno.
* **Escalabilidade Desacoplada:** A expansão do escopo do jogo (como a adição de novos animais ou novas categorias) é feita de forma declarativa. Basta inserir os novos arquivos `JSON` na origem e executar a rotina de reindexação do banco vetorial, dispensando alterações na lógica da aplicação ou processos refinamento da IA.
