from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """You are a precise assistant. Use only the provided context.
If the answer is not in the context, say you don't have enough evidence."""


def rag_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Question: {question}\n\nContext:\n{context}"),
        ]
    )
