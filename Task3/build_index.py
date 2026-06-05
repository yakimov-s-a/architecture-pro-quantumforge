import hashlib
import time
from pathlib import Path
from typing import Generator

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

# Для демонстрации оставляем значения в коде. В реальном приложении стоит вынести в переменные окружения.
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
CHROMA_DB_DIRECTORY = "../chroma_db"
COLLECTION_NAME = "knowledge_base"
DOCUMENTS_DIRECTORY = "../knowledge_base"

MARKDOWN_SPLITTER = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
        ("####", "h4"),
    ],
)
TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    length_function=lambda x: len(x.split()),

)

CHROMA_CLIENT = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    ),
    persist_directory=CHROMA_DB_DIRECTORY,
)


def get_documents() -> Generator[Document]:
    for path in Path(DOCUMENTS_DIRECTORY).iterdir():
        with open(path, "r", encoding="utf-8") as f:
            yield Document(page_content=f.read(), metadata={"source": path.name})


def split_markdown(document: Document) -> Generator[Document]:
    for markdown_section in MARKDOWN_SPLITTER.split_text(document.page_content):
        yield Document(
            page_content=markdown_section.page_content,
            metadata={**document.metadata, **markdown_section.metadata},
        )


def split_text(document: Document) -> Generator[Document]:
    for i, chunk in enumerate(TEXT_SPLITTER.split_documents([document])):
        yield Document(
            page_content=chunk.page_content,
            metadata={**chunk.metadata, **{"index": i}},
        )


def generate_id(chunk: Document) -> str:
    title = "_".join([
        chunk.metadata.get("source"),
        chunk.metadata.get("h1", ""),
        chunk.metadata.get("h2", ""),
        chunk.metadata.get("h3", ""),
        chunk.metadata.get("h4", ""),
        str(chunk.metadata.get("index")),
    ])

    return hashlib.sha256(title.encode("utf-8")).hexdigest()


def main():
    start = time.perf_counter()

    documents = get_documents()
    markdown_sections = (section for document in documents for section in split_markdown(document))
    chunks = [chunk for markdown_section in markdown_sections for chunk in split_text(markdown_section)]
    CHROMA_CLIENT.add_documents(documents=chunks, ids=[generate_id(chunk) for chunk in chunks])

    end = time.perf_counter()

    print(f"Number of chunks: {CHROMA_CLIENT._collection.count()}.")
    print(f"Elapsed time: {end - start} seconds.")


if __name__ == "__main__":
    main()
