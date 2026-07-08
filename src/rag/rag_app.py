import os
import requests
import sys

# --- 1. A ETAPA DE RECUPERAÇÃO (Ler a pasta inteira) ---
pasta_do_projeto = "/Users/hugoalmeida/Documents/trabalho_final_ip/Projeto_final_IP" 

codigo_completo = ""
ficheiros_lidos = 0

print("A procurar ficheiros de código na pasta...")

# O os.walk vai explorar a pasta principal e todas as subpastas
for raiz, pastas, ficheiros in os.walk(pasta_do_projeto):
    for ficheiro in ficheiros:
        # Aqui filtramos as extensões que queremos que a IA leia. 
        # Pode adicionar '.js', '.sql', '.html', etc., conforme a sua necessidade.
        if ficheiro.endswith(('.py', '.sql', '.json')): 
            caminho_completo = os.path.join(raiz, ficheiro)
            try:
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    # Adicionamos uma marcação para a IA saber qual ficheiro está a ler
                    codigo_completo += f"\n\n--- INÍCIO DO FICHEIRO: {ficheiro} ---\n"
                    codigo_completo += f.read()
                    codigo_completo += f"\n--- FIM DO FICHEIRO: {ficheiro} ---\n"
                    ficheiros_lidos += 1
            except Exception as e:
                print(f"Ignorado (erro ao ler): {ficheiro}")

if ficheiros_lidos == 0:
    print(f"❌ Não foram encontrados ficheiros de código válidos na pasta:\n{pasta_do_projeto}")
    sys.exit()

print(f"✅ Sucesso! {ficheiros_lidos} ficheiro(s) carregado(s) para a memória do Llama.")


# --- 2. CONFIGURAÇÃO DA LLM ---
url = "http://localhost:11434/api/generate"

print("=========================================================")
print("🤖 Chat Iniciado com o seu Projeto")
print("Faça perguntas sobre o seu código ou banco de dados.")
print("=========================================================\n")

while True:
    pergunta = input("Você: ")
    
    if pergunta.lower() in ['sair', 'exit', 'quit']:
        print("A encerrar...")
        sys.exit()
        
    if not pergunta.strip():
        continue

    # --- 3. CRIAR O PROMPT COM TODO O PROJETO ---
    prompt_enriquecido = f"""
    Você é um programador sénior. Abaixo está o código de vários ficheiros 
    do projeto do utilizador:

    {codigo_completo}

    Com base nestes ficheiros, responda à seguinte pergunta. Indique sempre 
    o nome do ficheiro relevante quando der a sua explicação.

    Pergunta: {pergunta}
    """

    dados = {
        "model": "llama3.1",
        "prompt": prompt_enriquecido,
        "stream": False
    }

    try:
        print("A analisar o projeto...")
        resposta = requests.post(url, json=dados)
        
        if resposta.status_code == 200:
            resultado = resposta.json()
            print(f"\nLlama 3.1: {resultado['response']}\n")
            print("-" * 50)
        else:
            print(f"Erro. Código: {resposta.status_code}\n")
            
    except Exception as erro:
        print(f"Erro de conexão: {erro}\n")