from __future__ import annotations

from typing import Iterable, List

from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from prompts import rag_prompt


def format_context(docs: Iterable[Document]) -> str:
    return "\n\n".join(
        f"Source: {doc.metadata.get('source','unknown')}\n{doc.page_content}"
        for doc in docs
    )


def build_rag_chain(retriever, llm: BaseChatModel):
    prompt = rag_prompt()
    return (
        {
            "context": retriever | RunnableLambda(format_context),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def cite_sources(docs: List[Document]) -> List[str]:
    return sorted({doc.metadata.get("source", "unknown") for doc in docs})
