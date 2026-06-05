from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Для демонстрации оставляем значения в коде. В реальном приложении стоит вынести в переменные окружения.
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
CHROMA_DB_DIRECTORY = "../chroma_db"
COLLECTION_NAME = "knowledge_base"

CHROMA_CLIENT = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    ),
    persist_directory=CHROMA_DB_DIRECTORY,
)


def main():
    query_text = "Who was Corin Planetrunner?"
    results = CHROMA_CLIENT.similarity_search(query=query_text, k=2)

    print(f"Query: {query_text}\n")
    for document in results:
        print(f"Chunk:\n{document.page_content}\n\nMetadata:")
        for key, value in document.metadata.items():
            print(f"{key}: {value}")
        print()


if __name__ == "__main__":
    main()
