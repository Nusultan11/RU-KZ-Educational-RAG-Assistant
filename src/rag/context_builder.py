"""Build LLM-ready RAG context objects from retrieved passages."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(frozen=True)
class RetrievedDocument:
    """A single document returned by the retriever."""

    doc_id: str
    text: str
    score: float
    source: str
    language: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def normalized_text(self) -> str:
        return " ".join(self.text.split())


@dataclass(frozen=True)
class RAGContext:
    """Context packet prepared for later prompt building and generation."""

    question: str
    documents: tuple[RetrievedDocument, ...]
    context_text: str
    max_context_chars: int
    truncated: bool
    omitted_documents: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "context_text": self.context_text,
            "max_context_chars": self.max_context_chars,
            "truncated": self.truncated,
            "omitted_documents": self.omitted_documents,
            "documents": [
                {
                    "doc_id": document.doc_id,
                    "score": document.score,
                    "source": document.source,
                    "language": document.language,
                    "text": document.text,
                    "metadata": document.metadata,
                }
                for document in self.documents
            ],
        }


class ContextBuilder:
    """Create a bounded text context from top-k retrieved documents."""

    def __init__(self, max_context_chars: int = 6000) -> None:
        if max_context_chars <= 0:
            raise ValueError("max_context_chars must be positive.")
        self.max_context_chars = max_context_chars

    def build(
        self,
        question: str,
        documents: Iterable[RetrievedDocument],
    ) -> RAGContext:
        question = question.strip()
        if not question:
            raise ValueError("question must not be empty.")

        selected_documents: list[RetrievedDocument] = []
        context_parts: list[str] = [f"Question:\n{question}", "", "Retrieved Context:"]
        current_length = sum(len(part) for part in context_parts)
        truncated = False
        omitted_documents = 0

        for rank, document in enumerate(documents, start=1):
            rendered = self._render_document(rank, document)
            extra_length = len(rendered) + 2
            if current_length + extra_length > self.max_context_chars:
                truncated = True
                omitted_documents += 1
                continue

            selected_documents.append(document)
            context_parts.append(rendered)
            current_length += extra_length

        return RAGContext(
            question=question,
            documents=tuple(selected_documents),
            context_text="\n\n".join(context_parts),
            max_context_chars=self.max_context_chars,
            truncated=truncated,
            omitted_documents=omitted_documents,
        )

    @staticmethod
    def _render_document(rank: int, document: RetrievedDocument) -> str:
        text = document.normalized_text()
        return (
            f"[{rank}]\n"
            f"Source: {document.source}\n"
            f"Document ID: {document.doc_id}\n"
            f"Language: {document.language}\n"
            f"Score: {document.score:.6f}\n"
            f"Text: {text}"
        )
