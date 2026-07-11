from pathlib import Path
import chromadb

from chunker import processar_arquivo
from embeddings import gerar_embedding

# Caminho da raiz do projeto
BASE_DIR = Path(__file__).resolve().parents[2]

# Pastas que serão indexadas
PASTAS = [
    BASE_DIR / "data",
    BASE_DIR / "src"
]

# Banco vetorial
client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))

try:
    client.delete_collection("projeto_ip")
except:
    pass

collection = client.get_or_create_collection(
    name="projeto_ip"

)

# Extensões aceitas
EXTENSOES = {
    ".py",
    ".json",
    ".html",
    ".css",
    ".js",
    ".md",
    ".txt",
    ".sql"
}


print("=" * 60)
print("INICIANDO INDEXAÇÃO")
print("=" * 60)

contador = 0

for pasta in PASTAS:

    for arquivo in pasta.rglob("*"):

        if not arquivo.is_file():
            continue

        if arquivo.suffix.lower() not in EXTENSOES:
            continue

        print(f"\nIndexando: {arquivo.relative_to(BASE_DIR)}")

        chunks = processar_arquivo(arquivo)

        for i, chunk in enumerate(chunks):

            embedding = gerar_embedding(chunk)

            collection.add(

                ids=[f"{arquivo.stem}_{i}"],

                embeddings=[embedding],

                documents=[chunk],

                metadatas=[

                    {
                        "arquivo": arquivo.name,
                        "caminho": str(arquivo.relative_to(BASE_DIR)),
                        "tipo": arquivo.suffix
                    }

                ]
            )

            contador += 1

print("\n")
print("=" * 60)
print(f"Finalizado! {contador} chunks indexados.")
print("=" * 60)