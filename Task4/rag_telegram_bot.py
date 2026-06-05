import textwrap

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Для демонстрации оставляем значения в коде. В реальном приложении стоит вынести в переменные окружения.
TELEGRAM_BOT_TOKEN = "<telegram_bot_token>"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
OLLAMA_BASE_URL = "http://localhost:11434"
LLM_MODEL = "gemma4:e2b"
CHROMA_DB_DIRECTORY = "../chroma_db"
COLLECTION_NAME = "knowledge_base"


def block(text: str) -> str:
    return textwrap.dedent(text)


EXAMPLES = [
    {
        "question": "What name did Corin Planetrunner take when he became a Varki?",
        "context": block("""
        A vergence in the Force, Corin Planetrunner was born on the desert planet of Oradin in the Outer Rim Territories in 41
        BBY. He was the son of Shmi Planetrunner, a slave who conceived a child without a father. His blood contained over
        twenty-thousand midi-chlorians, surpassing Grand Master Macio and all other Median in the galaxy.
        """).strip(),
        "answer": block("""
        Step-by-step reasoning:
        1. The user wants to know the name Corin Planetrunner took when he became a Varki.
        2. I will search the provided documents for information linking Corin Planetrunner, the Varki, and an adopted name or alter ego.
        3. Document 1 states: "His alter ego, Evilth Papa, the Dark Lord of the Varki, was created when Planetrunner turned to the dark side of the Force."
        4. The text identifies his alter ego as Evilth Papa.
        
        The name Corin Planetrunner took when he became associated with the Varki was Evilth Papa.
        """),
    },
    {
        "question": "Where was Drian Planetrunner born?",
        "context": block("""
        The son of Median Knight Corin Planetrunner and Senator Dan Liora, Drian Planetrunner was born along with his twin sister,
        Mira, in 19 BBY. As a result of Liora's death and Corin's fall to the dark side of the Force, the Planetrunner children
        were separated and sent into hiding, with Mira adopted by the royal family of Eryxara while Drian was raised by his
        relatives on Oradin.
        """).strip(),
        "answer": block("""
        Step-by-step reasoning:
        1. The user wants to know the birthplace of Drian Planetrunner.
        2. I will search the provided documents for information regarding Drian Planetrunner's birthplace.
        3. Document 1 discusses Corin Planetrunner's childhood on Oradin but does not specify Drian's birth location.
        4. Document 4 mentions that Drian Planetrunner spent his youth on the Lars' moisture farm, but this is not stated as his place of birth.
        5. Documents 2, 3, and 5 mention Drian in relation to other events or family lineage but do not explicitly state where he was born.
        6. Since the documents do not contain the specific information requested, I must state that I cannot find the answer.
        
        I couldn't find any confirmation.
        """),
    },
]
EXAMPLE_PROMPT = ChatPromptTemplate.from_messages([
    ("human", block("""
    ### <Documents>
    {context}
    
    ### <User question>
    {question}
    """)),
    ("ai", "{answer}"),
])
FEW_SHOT_PROMPT = FewShotChatMessagePromptTemplate(
    examples=EXAMPLES,
    example_prompt=EXAMPLE_PROMPT,
)

PROMPT = ChatPromptTemplate.from_messages([
    ("system", block("""
    ### Role
    You are a RAG assistant.
    You always think first and then respond. Always write down your steps.
    Your job is to accurately answer the user's question using ONLY the information in the provided documents.
    If the documents don't contain the required information, honestly say, "I couldn't find any confirmation."
    Avoid speculation and hallucinations.
    
    ### Algorithm
    1. Carefully read all documents in the <Documents> section.
    2. Determine which of them are truly relevant to the question.
    3. Briefly summarize the key facts (do not show them to the user).
    4. Formulate a final answer in English, relying only on the supported facts.
    
    ### Output format
    First write your reasoning step by step, then on a new line write the short answer on question (1-3 sentences).
    """)),
    FEW_SHOT_PROMPT,
    ("human", block("""
    ### <Documents>
    {context}
    
    ### <User question>
    {question}
    """)),
])

CHROMA_CLIENT = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    ),
    persist_directory=CHROMA_DB_DIRECTORY,
)

RETRIEVER = CHROMA_CLIENT.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 15},
)

CHAT_LLM = ChatOllama(
    model=LLM_MODEL,
    base_url="http://localhost:11434",
    temperature=0,
)


async def chat(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    query = update.message.text
    if not query:
        return

    chunks = await RETRIEVER.ainvoke(query)

    context_documents = []
    for i, chunk in enumerate(chunks, start=1):
        context_document = f"{i}. Source: {chunk.metadata.get("source")}"
        h1 = chunk.metadata.get("h1")
        if h1:
            context_document += f" / {h1}"
        h2 = chunk.metadata.get("h2")
        if h2:
            context_document += f" / {h2}"
        h3 = chunk.metadata.get("h3")
        if h3:
            context_document += f" / {h3}"
        h4 = chunk.metadata.get("h4")
        if h4:
            context_document += f" / {h4}"
        context_document += f"\n{chunk.page_content}"
        context_documents.append(context_document)
    context = "\n\n".join(context_documents)

    chain = PROMPT | CHAT_LLM
    response = await chain.ainvoke({"question": query, "context": context})
    await update.message.reply_text(str(response.content))


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()


if __name__ == "__main__":
    main()
