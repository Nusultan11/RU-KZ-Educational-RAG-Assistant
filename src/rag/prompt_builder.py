"""Build LLM prompts from prepared RAG contexts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .context_builder import RAGContext


@dataclass(frozen=True)
class RAGPrompt:
    """A prompt packet ready to be passed to a generator later."""

    question: str
    prompt_text: str
    context_text: str
    instruction: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "prompt_text": self.prompt_text,
            "context_text": self.context_text,
            "instruction": self.instruction,
            "metadata": self.metadata,
        }


class PromptBuilder:
    """Create a deterministic prompt from a RAGContext."""

    def __init__(
        self,
        instruction: str,
        answer_language_policy: str = "Answer in the same language as the question.",
        require_sources: bool = True,
    ) -> None:
        instruction = instruction.strip()
        answer_language_policy = answer_language_policy.strip()
        if not instruction:
            raise ValueError("instruction must not be empty.")
        if not answer_language_policy:
            raise ValueError("answer_language_policy must not be empty.")

        self.instruction = instruction
        self.answer_language_policy = answer_language_policy
        self.require_sources = require_sources

    def build(self, context: RAGContext, question: str | None = None) -> RAGPrompt:
        final_question = (question or context.question).strip()
        if not final_question:
            raise ValueError("question must not be empty.")
        if not context.context_text.strip():
            raise ValueError("context.context_text must not be empty.")

        source_instruction = (
            "Cite the retrieved context item numbers you used."
            if self.require_sources
            else "Do not add citations unless they are already present in the context."
        )
        prompt_text = "\n\n".join(
            [
                "System instruction:",
                self.instruction,
                self.answer_language_policy,
                source_instruction,
                "If the retrieved context is insufficient, say that the answer is not available in the provided context.",
                context.context_text,
                "Answer:",
            ],
        )

        return RAGPrompt(
            question=final_question,
            prompt_text=prompt_text,
            context_text=context.context_text,
            instruction=self.instruction,
            metadata={
                "documents": len(context.documents),
                "context_truncated": context.truncated,
                "omitted_documents": context.omitted_documents,
                "require_sources": self.require_sources,
            },
        )
