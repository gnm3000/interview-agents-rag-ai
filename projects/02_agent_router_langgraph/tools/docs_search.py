from pydantic import BaseModel, Field


class DocsSearchInput(BaseModel):
    query: str = Field(..., description="Docs query")


def run_docs_search(input_data: DocsSearchInput) -> str:
    return f"Found docs for '{input_data.query}'."  # TODO: connect to RAG
