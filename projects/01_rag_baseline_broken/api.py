from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from chunking import split_documents
from ingest import load_documents, normalize_metadata
from rag_chain import build_rag_chain, cite_sources
from retriever import build_retriever
from vectorstore import get_vectorstore, upsert_documents

app = FastAPI()
DATA_DIR = Path(__file__).parent / "data" / "sample_docs"
PERSIST_DIR = Path(__file__).parent / ".chroma"


def build_index():
    documents = normalize_metadata(load_documents(DATA_DIR))
    chunks = split_documents(documents)
    embedding = OpenAIEmbeddings()
    vectorstore = get_vectorstore(persist_directory=PERSIST_DIR, embedding=embedding)
    upsert_documents(vectorstore, chunks)
    return build_retriever(vectorstore), vectorstore


@app.post("/ask")
async def ask(question: str):
    retriever, _ = build_index()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = build_rag_chain(retriever, llm)
    answer = chain.invoke(question)
    docs = retriever.get_relevant_documents(question)
    return {"answer": answer, "sources": cite_sources(docs)}
